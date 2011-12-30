=====================
HTMLテンプレート管理
=====================

色々なところで見かけた使えそうなHTMLテンプレートをダウンロードするも、すぐにどこに保存したか忘れたり、そもそもダウンロードしたことすら忘れる。
そんな私のためのHTMLテンプレート管理ツールです。

---------------------
特徴
---------------------
* ちょーシンプル
* 「テンプレート名」と「テンプレート本体(zip圧縮)」の入力でOK
* テンプレートファイル（zip圧縮)を展開してデモページを作成。
* デモページからスクリーンショットを撮ってサムネイルを作成。
* 最低限の手間で、なんとなく良い感じ
* タグ入力で分類も可能（でも、これは雑な作り）

---------------------
今後
---------------------
* ライセンスは簡単に入力できるようにしたい。
* 入力の最低限はHTMLテンプレートだけにしたい。
* 入力時、ドラッグ＆ドロップでzipファイルを投げ込むとそのデータを展開してスクリーンショット付きの入力エリアが、ぽんぽん、とできあがってそこに追加情報を入力しておわりっ♪、にしたい。
* 平行して、twitterとfacebookでのアカウント作成ができる一般公開用も作ってはいるけど、zipファイルの中身チェックしたり、サイズとか考えたりするのを考えるとちょっと面倒
* wkhtmltoimageは無理にしても、なんかこう、setup.pyでinstallしたらウェブサーバーがデーモンで動くようなセットアップしたい。
* というわけで、続きはだれか作っ(ry

---------------------
使ってるもの
---------------------
* python
    * Flask
    * SQLAlchemy
* twitter-bootstrap
* jquery
* wkhtmltoimage

---------------------
動かし方（めんどう）
---------------------

１．さくらのクラウドでサーバを作る
==================================
　どこでもいいけどね。以下はテンプレートからSientific Linux 6.1を使った場合です。

２．環境の準備
==================================
　さくらのクラウドのテンプレートでは、Development toolsやgitあたりは最初からインストール済のようです。
　もしmakeができなければ、yum groupinstall "Development Tools" をすればmakeに必要なものはだいたい揃う気がします。
　あと、iptablesとかそういうのは省略！


２．１　pythonのインストール
----------------------------------
デフォルトでもインストールされているけど、python2.7をインストールして使います。::

	wget http://python.org/ftp/python/2.7.2/Python-2.7.2.tar.bz2tar jxf Python-2.7.2.tar.bz2
	cd Python-2.7.2
	./configure --prefix=/opt/python2.7 --with-threads --enable-shared
	make && make install
	echo "/opt/python2.7/lib/" > /etc/ld.so.conf.d/python2.7.conf
	cd
	wget http://peak.telecommunity.com/dist/ez_setup.py
	/opt/python2.7/bin/python ez_setup.py
	/opt/python2.7/bin/easy_install pip
	/opt/python2.7/bin/pip install virtualenv


２．２　wkhtmltoimageのインストール
----------------------------------
　スクリーンショットを撮るのに使います。qtが結構時間かかります。::

	# qt, wkhtmltopdf, wkhtmltoimage のinstall
	# とても時間がかかります。

	mkdir /var/src
	cd /var/src

	yum install -y openssl-devel libXrender-devel libXext-devel libXft-devel

	git clone git://github.com/antialize/wkhtmltopdf.git wkhtmltopdf
	git clone git://gitorious.org/+wkhtml2pdf/qt/wkhtmltopdf-qt.git wkhtmltopdf-qt

	cd wkhtmltopdf-qt
	./configure -nomake tools,examples,demos,docs,translations -opensource -prefix "../wkqt"
	make -j3 && make install

	cd ../wkhtmltopdf
	../wkqt/bin/qmake
	make && make install

	# キャプチャ用にfontインストール
	# さくらのクラウドのテンプレートの場合、IPAフォントが最初から入ってる。
	# 他に入れたいフォントがあれば /usr/share/fonts に追加する。
	yum install urw-fonts


２．３　apache+mod_wsgiのインストール
----------------------------------
　nginxでもなんでもいいけど、定番ってことで。::

	# apacheのインストール
	yum install httpd

	# yumにもmod_wsgiはあるけど、python2.7用にソースから作り直します。
	yum install -y apr-devel apr-util-devel httpd-devel
	wget http://modwsgi.googlecode.com/files/mod_wsgi-3.3.tar.gz

	tar zxf mod_wsgi-3.3.tar.gz
	./configure --with-apxs=/usr/sbin/apxs --with-python=/opt/python2.7/bin/python
	echo "LoadModule wsgi_module modules/mod_wsgi.so" > /etc/httpd/conf.d/wsgi.conf


３．templaを取得
==================================
やっと今回作ったやつのソースを取得::

	cd /var/www/
	git clone git://github.com/planset/templa.git


４．動作環境を作成
==================================
::

	# virtualenvを使って、必要なライブラリを整えます。
	cd /var/www
	/opt/python2.7/bin/virtualenv --distribute --no-site-packages --python=/opt/python2.7/bin/python templa
	cd templa
	source bin/activate

	# 以降はvirtualenv環境で実行

	# 必要なライブラリをインストール
	pip install Flask SQLAlchemy Flask-WTF Flask-SQLAlchemy Flask-script Flask-Uploads

	# DBはsqlite3を使うのでライブラリをインストール
	yum install sqlite-devel
	pip install pysqlite

	# 画像を扱うためのPILはzlibとlibjpegを使えるようにしたいので、pipからではなくソースからインストールする。
	yum install zlib-devel libjpeg-devel

	wget http://effbot.org/downloads/Imaging-1.1.7.tar.gz
	tar zxf Imaging-1.1.7.tar.gz 
	cd Imaging-1.1.7

	vi setup.py

	# 以下を変更する。
	JPEG_ROOT = "/usr/lib64", "/usr/include"
	ZLIB_ROOT = "/usr/lib64", "/usr/include"

	# setup.py保存後以下を実行
	python setup.py install


	# データベースとかの設定
	python manage.py init
	python manage.py adminpassword
	# ８文字以上のバスワード入力

	# もし、Internal Server Errorとかでたら、書き込み権限かもしれないので、以下を実行。たぶん大丈夫・・・だといいな。
	# chown -R apache:apache /var/www/templa



５．apacheの設定
==================================
　最後にapacheにpythonアプリを動かす設定を追加します。::

	cat << END >> /etc/httpd/conf/httpd.conf
	NameVirtualHost *:80
	<VirtualHost *:80>
	    Alias /static/ /var/www/templa/app/static/
	    Alias /static_demo/ /var/www/templa/app/static_demo/
	    WSGIScriptAlias / /var/www/templa/wsgi.py
	    <Directory "/var/www/templa">
	        Order allow,deny
	        Allow from all
	        WSGIScriptReloading On
	    </Directory>
	</VirtualHost>
	END

	service httpd restart


６．動かしてみる。
==================================
ブラウザで http://[ip]/ を開く。



---------------------
使い方
---------------------
* adminログインしてテンプレートを追加する。
* テンプレートを見る。
* スクリーンショットとか： http://lowlevellife.com/?p=1480

---------------------
使い方 デバック起動
---------------------
　apacheの設定以外を行った上で、::

    cd /var/www/templa
    source bin/activate
    python manage.py runserver

　これだと127.0.0.1で起動する（ローカルからしかアクセスできない）。外部からもアクセスさせたいのであれば、::

    python manage.py runserver -h 0.0.0.0












