import os

SMALI = r'decompiled_clean\smali\org\xbmc\kodi\Splash$FillCache.smali'

with open(SMALI, 'r') as f:
    lines = f.readlines()

content = ''.join(lines)

# Find the insertion point: right before ".line 365" / "iget-object v0, p0, ... this$0" / "const/4 v1, 0x6"
# The copy should happen inside the try block, after setLastModified

old = '''    :try_end_2
    .catch Ljava/io/FileNotFoundException; {:try_start_2 .. :try_end_2} :catch_2
    .catch Ljava/io/IOException; {:try_start_2 .. :try_end_2} :catch_1

    .line 365
    iget-object v0, p0, Lorg/xbmc/kodi/Splash$FillCache;->this$0:Lorg/xbmc/kodi/Splash;

    const/4 v1, 0x6'''

new = '''    :try_end_2
    .catch Ljava/io/FileNotFoundException; {:try_start_2 .. :try_end_2} :catch_2
    .catch Ljava/io/IOException; {:try_start_2 .. :try_end_2} :catch_1

    .line 364
    iget-object v8, p0, Lorg/xbmc/kodi/Splash$FillCache;->mSplash:Lorg/xbmc/kodi/Splash;

    invoke-virtual {v8}, Lorg/xbmc/kodi/Splash;->getFilesDir()Ljava/io/File;

    move-result-object v8

    new-instance v9, Ljava/lang/StringBuilder;

    invoke-direct {v9}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v9, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/Object;)Ljava/lang/StringBuilder;

    const-string v8, "/.kodi/userdata/Database"

    invoke-virtual {v9, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v9}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v8

    new-instance v9, Ljava/io/File;

    invoke-direct {v9, v8}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v9}, Ljava/io/File;->mkdirs()Z

    new-instance v9, Ljava/io/File;

    new-instance v10, Ljava/lang/StringBuilder;

    invoke-direct {v10}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v10, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v8, "/Addons33.db"

    invoke-virtual {v10, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v10}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v8

    invoke-direct {v9, v8}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v9}, Ljava/io/File;->exists()Z

    move-result v10

    if-eqz v10, :copy_done

    iget-object v10, p0, Lorg/xbmc/kodi/Splash$FillCache;->this$0:Lorg/xbmc/kodi/Splash;

    invoke-static {v10}, Lorg/xbmc/kodi/Splash;->access$1300(Lorg/xbmc/kodi/Splash;)Ljava/lang/String;

    move-result-object v10

    new-instance v11, Ljava/io/File;

    new-instance v12, Ljava/lang/StringBuilder;

    invoke-direct {v12}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v12, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v10, "/userdata/Database/Addons33.db"

    invoke-virtual {v12, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v12}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v10

    invoke-direct {v11, v10}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v11}, Ljava/io/File;->exists()Z

    move-result v12

    if-eqz v12, :copy_done

    new-instance v12, Ljava/io/FileInputStream;

    invoke-direct {v12, v11}, Ljava/io/FileInputStream;-><init>(Ljava/io/File;)V

    new-instance v13, Ljava/io/FileOutputStream;

    invoke-direct {v13, v9}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V

    const/16 v14, 0x2000

    new-array v14, v14, [B

    :copy_loop

    invoke-virtual {v12, v14}, Ljava/io/FileInputStream;->read([B)I

    move-result v15

    if-lez v15, :cond_copy_close

    const/16 v16, 0x0

    move-object/from16 v17, v14

    move/from16 v18, v15

    invoke-virtual {v13, v17, v16, v18}, Ljava/io/FileOutputStream;->write([BII)V

    goto :copy_loop

    :cond_copy_close

    invoke-virtual {v13}, Ljava/io/FileOutputStream;->close()V

    invoke-virtual {v12}, Ljava/io/FileInputStream;->close()V

    :copy_done

    .line 365
    iget-object v0, p0, Lorg/xbmc/kodi/Splash$FillCache;->this$0:Lorg/xbmc/kodi/Splash;

    const/4 v1, 0x6'''

if old not in content:
    print("ERROR: target not found")
    exit(1)

content = content.replace(old, new, 1)

with open(SMALI, 'w') as f:
    f.write(content)

print("Patched successfully")
