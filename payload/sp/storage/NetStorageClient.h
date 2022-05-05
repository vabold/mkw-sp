#pragma once

#include <Common.h>
#include <sp/Tcp.h>
#include <string.h>

//
// Stream buffer
//

enum {
    NET_STREAM_CHUNK = 1024,
};

typedef struct {
    s32 streamedOffset;
    s32 streamedSize;
    u8 buffer[NET_STREAM_CHUNK];
} NetStreamBuf;

void NetStreamBuf_copy(NetStreamBuf *self, const NetStreamBuf *other);
bool NetStreamBuf_contains(NetStreamBuf *buf, s32 offset, s32 len);

//
// Storage client
//

typedef struct {
    u32 filesInFlight;
    TcpSocket sock;
    OSMutex mutex;
} NetStorageClient;

void NetStorageClient_create(NetStorageClient *client);
void NetStorageClient_destroy(NetStorageClient *client);

bool NetStorageClient_connect(
        NetStorageClient *client, u8 ipa, u8 ipb, u8 ipc, u8 ipd, u32 port);
void NetStorageClient_disconnect(NetStorageClient *client);

//
// Net file
//

typedef struct {
    NetStorageClient *client;
    u32 isOpen;
    s32 id;

    s32 fileSize; // Folders: Value is meaningless, just needs to be nonzero
} NetNode;

typedef struct {  // Zero initialized
    NetNode node;
    NetStreamBuf buffer;
} NetFile;

static inline void NetFile_create(NetFile *file) {
    memset(file, 0, sizeof(*file));
}
bool NetFile_open(NetFile *file, NetStorageClient *client, const wchar_t *path);
void NetFile_close(NetFile *file);
u32 NetFile_read(NetFile *file, void *dst, s32 len, s32 offset);
// Prefetch
bool NetFile_stream(NetFile *file, u32 pos, u32 bytes);

bool NetFile_rename(NetFile *file, const wchar_t *path);
bool NetFile_removeAndClose(NetFile *file);

bool NetFile_write(NetFile *file, const void *src, u32 size, u32 offset);

typedef struct {
    NetNode node;
} NetDir;

typedef struct {
    wchar_t name[255 + 1];
    bool isDir;
} NetDirEntry;

bool NetDir_open(NetDir *dir, NetStorageClient *client, const wchar_t *path);
bool NetDir_read(NetDir *dir, NetDirEntry *out);
void NetDir_close(NetDir *dir);

bool NetStorage_sendJSONCommandsUTF16(NetStorageClient *self, const wchar_t *str);
bool NetStorage_sendJSONCommands(NetStorageClient *self, const char *str);