import os
import glob

SMALI = os.path.join('decompiled_kodi_new', 'smali', 'org', 'xbmc', 'kodi', 'Splash$FillCache.smali')

with open(SMALI, 'r') as f:
    content = f.read()

# DO NOT increase .locals - just reuse existing registers v0-v3
# Insert right before ".line 365" state=6
# We'll use v0,v1,v2,v3 which are free after setLastModified

old = '''    .line 365
    iget-object v0, p0, Lorg/xbmc/kodi/Splash$FillCache;->this$0:Lorg/xbmc/kodi/Splash;

    const/4 v1, 0x6'''

# Minimal copy using only v0-v3
# v0 = dest File
# v1 = src File  
# v2 = FileInputStream
# v3 = FileOutputStream
new = '''    iget-object v0, p0, Lorg/xbmc/kodi/Splash$FillCache;->mSplash:Lorg/xbmc/kodi/Splash;

    invoke-virtual {v0}, Lorg/xbmc/kodi/Splash;->getFilesDir()Ljava/io/File;

    move-result-object v0

    new-instance v1, Ljava/io/File;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const-string v0, "/.kodi/userdata/Database/Addons33.db"

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {v1, v0}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1}, Ljava/io/File;->getParentFile()Ljava/io/File;

    move-result-object v0

    invoke-virtual {v0}, Ljava/io/File;->mkdirs()Z

    invoke-virtual {v1}, Ljava/io/File;->exists()Z

    move-result v0

    if-eqz v0, :copy_done

    iget-object v0, p0, Lorg/xbmc/kodi/Splash$FillCache;->this$0:Lorg/xbmc/kodi/Splash;

    invoke-static {v0}, Lorg/xbmc/kodi/Splash;->access$1300(Lorg/xbmc/kodi/Splash;)Ljava/lang/String;

    move-result-object v0

    new-instance v1, Ljava/io/File;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v0, "/userdata/Database/Addons33.db"

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-direct {v1, v0}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1}, Ljava/io/File;->exists()Z

    move-result v0

    if-eqz v0, :copy_done

    new-instance v0, Ljava/io/FileInputStream;

    invoke-direct {v0, v1}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    new-instance v2, Ljava/io/File;

    new-instance v3, Ljava/lang/StringBuilder;

    invoke-direct {v3}, Ljava/lang/StringBuilder;-><init>()V

    iget-object v1, p0, Lorg/xbmc/kodi/Splash$FillCache;->mSplash:Lorg/xbmc/kodi/Splash;

    invoke-virtual {v1}, Lorg/xbmc/kodi/Splash;->getFilesDir()Ljava/io/File;

    move-result-object v1

    invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const-string v1, "/.kodi/userdata/Database/Addons33.db"

    invoke-virtual {v3, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {v2, v1}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    new-instance v1, Ljava/io/FileOutputStream;

    invoke-direct {v1, v2}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V

    const/16 v2, 0x2000

    new-array v2, v2, [B

    :copy_loop

    invoke-virtual {v0, v2}, Ljava/io/FileInputStream;->read([B)I

    move-result v3

    if-lez v3, :copy_close

    const/4 v4, 0x0

    invoke-virtual {v1, v2, v4, v3}, Ljava/io/FileOutputStream;->write([BII)V

    goto :copy_loop

    :copy_close

    invoke-virtual {v1}, Ljava/io/FileOutputStream;->close()V

    invoke-virtual {v0}, Ljava/io/FileInputStream;->close()V

    :copy_done

    .line 365
    iget-object v0, p0, Lorg/xbmc/kodi/Splash$FillCache;->this$0:Lorg/xbmc/kodi/Splash;

    const/4 v1, 0x6'''

if old not in content:
    print("ERROR: target not found")
    exit(1)

content = content.replace(old, new, 1)

# DON'T change .locals - keep it at 12 but our code only uses v0-v4

with open(SMALI, 'w') as f:
    f.write(content)

print("Patched with minimal registers (v0-v4 only)")
