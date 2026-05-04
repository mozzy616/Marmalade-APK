import os

SMALI_PATH = r'decompiled_clean\smali\org\xbmc\kodi\Splash$FillCache.smali'

with open(SMALI_PATH, 'r') as f:
    content = f.read()

# 1. Add the CopyUserDataFiles method before the final .end method markers
copy_method = '''
.method private CopyUserDataFiles()V
    .locals 10

    iget-object v0, p0, Lorg/xbmc/kodi/Splash$FillCache;->mSplash:Lorg/xbmc/kodi/Splash;

    invoke-virtual {v0}, Lorg/xbmc/kodi/Splash;->getFilesDir()Ljava/io/File;

    move-result-object v0

    new-instance v1, Ljava/io/File;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const-string v0, "/.kodi/userdata/Database"

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {v1, v0}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1}, Ljava/io/File;->mkdirs()Z

    new-instance v2, Ljava/io/File;

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v3, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v4, "/Addons33.db"

    invoke-virtual {v3, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    invoke-direct {v2, v3}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v2}, Ljava/io/File;->exists()Z

    move-result v3

    if-eqz v3, :copy_done

    iget-object v3, p0, Lorg/xbmc/kodi/Splash$FillCache;->this$0:Lorg/xbmc/kodi/Splash;

    invoke-static {v3}, Lorg/xbmc/kodi/Splash;->access$1300(Lorg/xbmc/kodi/Splash;)Ljava/lang/String;

    move-result-object v3

    new-instance v4, Ljava/io/File;

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v5, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v6, "/userdata/Database/Addons33.db"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-direct {v4, v5}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v4}, Ljava/io/File;->exists()Z

    move-result v6

    if-eqz v6, :copy_done

    new-instance v6, Ljava/io/FileInputStream;

    invoke-direct {v6, v4}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    new-instance v7, Ljava/io/FileOutputStream;

    invoke-direct {v7, v2}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V

    const/16 v8, 0x2000

    new-array v8, v8, [B

    :copy_loop

    invoke-virtual {v6, v8}, Ljava/io/FileInputStream;->read([B)I

    move-result v9

    if-lez v9, :cond_close

    const/4 v10, 0x0

    invoke-virtual {v7, v8, v10, v9}, Ljava/io/FileOutputStream;->write([BII)V

    goto :copy_loop

    :cond_close

    invoke-virtual {v7}, Ljava/io/FileOutputStream;->close()V

    invoke-virtual {v6}, Ljava/io/FileInputStream;->close()V

    :copy_done

    return-void
.end method

'''

# Insert before the last .end method
# Find the last occurrence of .end method
last_end = content.rfind('.end method')
if last_end == -1:
    print("ERROR: Could not find .end method")
    exit(1)

# Find the position after the last .end method's newline
insert_pos = content.find('\n', last_end) + 1

content = content[:insert_pos] + copy_method + content[insert_pos:]

# 2. Add the call to CopyUserDataFiles before setting state to 6
# Find the target block
target = '''    .line 365
    iget-object v0, p0, Lorg/xbmc/kodi/Splash$FillCache;->this$0:Lorg/xbmc/kodi/Splash;

    const/4 v1, 0x6

    invoke-static {v0, v1}, Lorg/xbmc/kodi/Splash;->access$002(Lorg/xbmc/kodi/Splash;I)I'''

replacement = '''    .line 364
    invoke-direct {p0}, Lorg/xbmc/kodi/Splash$FillCache;->CopyUserDataFiles()V

    .line 365
    iget-object v0, p0, Lorg/xbmc/kodi/Splash$FillCache;->this$0:Lorg/xbmc/kodi/Splash;

    const/4 v1, 0x6

    invoke-static {v0, v1}, Lorg/xbmc/kodi/Splash;->access$002(Lorg/xbmc/kodi/Splash;I)I'''

if target not in content:
    print("ERROR: Could not find target insertion point")
    exit(1)

content = content.replace(target, replacement, 1)

with open(SMALI_PATH, 'w') as f:
    f.write(content)

print("Successfully patched Splash$FillCache.smali")
