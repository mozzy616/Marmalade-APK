.class public Lorg/xbmc/kodi/BuildExtractor;
.super Ljava/lang/Object;
.source "BuildExtractor.java"

.method public static extract(Landroid/content/Context;)V
    .locals 10

    invoke-virtual {p0}, Landroid/content/Context;->getCacheDir()Ljava/io/File;
    move-result-object v0
    invoke-virtual {v0}, Ljava/io/File;->getAbsolutePath()Ljava/lang/String;
    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;
    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V
    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v0, "/apk"
    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v5

    new-instance v1, Ljava/lang/StringBuilder;
    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V
    invoke-virtual {v1, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v2, "/.build_extracted"
    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v6

    new-instance v1, Ljava/io/File;
    invoke-direct {v1, v6}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1}, Ljava/io/File;->exists()Z
    move-result v0
    if-eqz v0, :cond_0
    return-void

    :cond_0
    :try_start_0
    invoke-virtual {p0}, Landroid/content/Context;->getAssets()Landroid/content/res/AssetManager;
    move-result-object v0
    const-string v1, "custom_build.zip"
    invoke-virtual {v0, v1}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;
    move-result-object v0

    invoke-virtual {p0}, Landroid/content/Context;->getCacheDir()Ljava/io/File;
    move-result-object v1
    new-instance v2, Ljava/lang/StringBuilder;
    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V
    invoke-virtual {v2, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v3, "/_build_tmp.zip"
    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v8

    new-instance v1, Ljava/io/File;
    invoke-direct {v1, v8}, Ljava/io/File;-><init>(Ljava/lang/String;)V
    new-instance v2, Ljava/io/FileOutputStream;
    invoke-direct {v2, v1}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V

    const/16 v1, 0x2000
    new-array v9, v1, [B

    :goto_0
    invoke-virtual {v0, v9}, Ljava/io/InputStream;->read([B)I
    move-result v3
    const/4 v4, -0x1
    if-le v3, v4, :cond_2
    const/4 v4, 0x0
    invoke-virtual {v2, v9, v4, v3}, Ljava/io/FileOutputStream;->write([BII)V
    goto :goto_0

    :cond_2
    invoke-virtual {v2}, Ljava/io/FileOutputStream;->close()V
    invoke-virtual {v0}, Ljava/io/InputStream;->close()V

    new-instance v0, Ljava/util/zip/ZipFile;
    invoke-direct {v0, v1}, Ljava/util/zip/ZipFile;-><init>(Ljava/io/File;)V
    invoke-virtual {v0}, Ljava/util/zip/ZipFile;->entries()Ljava/util/Enumeration;
    move-result-object v2

    :goto_1
    invoke-interface {v2}, Ljava/util/Enumeration;->hasMoreElements()Z
    move-result v3
    if-eqz v3, :cond_5

    invoke-interface {v2}, Ljava/util/Enumeration;->nextElement()Ljava/lang/Object;
    move-result-object v3
    check-cast v3, Ljava/util/zip/ZipEntry;

    invoke-virtual {v3}, Ljava/util/zip/ZipEntry;->getName()Ljava/lang/String;
    move-result-object v4
    new-instance v3, Ljava/io/File;
    new-instance v7, Ljava/lang/StringBuilder;
    invoke-direct {v7}, Ljava/lang/StringBuilder;-><init>()V
    invoke-virtual {v7, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    const-string v8, "/"
    invoke-virtual {v7, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v7, v4}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v7}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object v7
    invoke-direct {v3, v7}, Ljava/io/File;-><init>(Ljava/lang/String;)V

    invoke-virtual {v3}, Ljava/io/File;->getParentFile()Ljava/io/File;
    move-result-object v7
    invoke-virtual {v7}, Ljava/io/File;->mkdirs()Z

    new-instance v7, Ljava/io/FileOutputStream;
    invoke-direct {v7, v3}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V
    invoke-virtual {v0, v4}, Ljava/util/zip/ZipFile;->getInputStream(Ljava/util/zip/ZipEntry;)Ljava/io/InputStream;
    move-result-object v3

    :goto_2
    invoke-virtual {v3, v9}, Ljava/io/InputStream;->read([B)I
    move-result v4
    const/4 v8, -0x1
    if-le v4, v8, :cond_3
    const/4 v8, 0x0
    invoke-virtual {v7, v9, v8, v4}, Ljava/io/FileOutputStream;->write([BII)V
    goto :goto_2

    :cond_3
    invoke-virtual {v7}, Ljava/io/FileOutputStream;->close()V
    goto :goto_1

    :cond_5
    invoke-virtual {v0}, Ljava/util/zip/ZipFile;->close()V

    new-instance v0, Ljava/io/File;
    invoke-direct {v0, v8}, Ljava/io/File;-><init>(Ljava/lang/String;)V
    invoke-virtual {v0}, Ljava/io/File;->delete()Z

    new-instance v0, Ljava/io/FileWriter;
    invoke-direct {v0, v6}, Ljava/io/FileWriter;-><init>(Ljava/lang/String;)V
    const-string v1, "done"
    invoke-virtual {v0, v1}, Ljava/io/FileWriter;->write(Ljava/lang/String;)V
    invoke-virtual {v0}, Ljava/io/FileWriter;->close()V

    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0
    goto :goto_3

    :catch_0
    move-exception v0

    :goto_3
    return-void
.end method
