
JDK_URL=http://download.oracle.com/otn-pub/java/jdk/6u38-b05/jdk-6u38-linux-x64.bin
JDK_BIN=$(shell basename $(JDK_URL))

$(JDK_BIN): 
	wget -O $(JDK_BIN) -c --no-cookies --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com" $(JDK_URL) 

jdk: $(JDK_BIN)
	test -d /usr/lib/jvm/jdk6 || (yes | bash -x ./$(JDK_BIN) && mv jdk1.6.0_38 /usr/lib/jvm/jdk6)
	echo "export JAVA_HOME=/usr/lib/jvm/jdk6/"> /etc/profile.d/java.sh 

epel:
	test -f /etc/yum.repos.d/epel.repo || rpm -ivh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
	yum makecache

git: epel
	yum -y install git-core gcc gcc-c++ pdsh 

maven: jdk
	wget -c http://apache.techartifact.com/mirror/maven/maven-3/3.0.4/binaries/apache-maven-3.0.4-bin.tar.gz
	-- mkdir /opt/hadoop-build/
	tar -C /opt/hadoop-build/ --strip-components=1 -xzvf apache-maven-3.0.4-bin.tar.gz

protobuf: git 
	wget -c http://protobuf.googlecode.com/files/protobuf-2.4.1.tar.bz2
	tar -xvf protobuf-2.4.1.tar.bz2
	export PATH=$$PATH:/usr/bin/; cd protobuf-2.4.1; \
	./configure --prefix=/opt/hadoop-build/; \
	make -j4; \
	make install

hadoop: git maven protobuf
	test -d hadoop || git clone git://git.apache.org/hadoop-common.git hadoop 
	cd hadoop; git pull --rebase
	export PATH=$$PATH:/opt/hadoop-build/bin/; \
	cd hadoop/; git branch branch-2 --track origin/branch-2; \
	git checkout branch-2; \
	. /etc/profile; \
	mvn package -Pdist -DskipTests;


hadoop/hadoop-dist/target/: 
	make hadoop

install: hadoop/hadoop-dist/target/
	rsync -avP hadoop/hadoop-dist/target/hadoop-2*/ /opt/hadoop/
	cp slaves gen-conf.py /opt/hadoop/etc/hadoop/
	cd /opt/hadoop/etc/hadoop/; python gen-conf.py

/opt/hadoop: install

/root/.ssh/id_rsa: 
	ssh-keygen -f /root/.ssh/id_rsa -N ''
	echo "StrictHostKeyChecking=no" >> ~/.ssh/config

propogate: /opt/hadoop slaves /root/.ssh/id_rsa
	cp slaves /opt/hadoop/etc/hadoop/;
	ssh-copy-id localhost;
	for host in $$(cat slaves | grep -v localhost) ; do \
		rsync -avP ~/.ssh/ ~/.ssh/; \
		rsync --exclude \*.log -avP /opt/ $$host:/opt/; \
		rsync -avP /usr/lib/jvm/jdk6/ $$host:/usr/lib/jvm/jdk6/; \
		scp /etc/profile.d/java.sh $$host:/etc/profile.d/java.sh; \
	done

start: propogate
	test -d /grid/0/tmp/dfs/name/current/ || /opt/hadoop/bin/hdfs namenode -format
	/opt/hadoop/sbin/hadoop-daemon.sh start namenode
	/opt/hadoop/sbin/yarn-daemon.sh start resourcemanager
	/opt/hadoop/sbin/mr-jobhistory-daemon.sh start historyserver
	pdsh -w $$(tr \\n , < slaves) '/opt/hadoop/sbin/hadoop-daemon.sh start datanode && /opt/hadoop/sbin/yarn-daemon.sh start nodemanager'

stop:
	/opt/hadoop/sbin/hadoop-daemon.sh stop namenode
	/opt/hadoop/sbin/yarn-daemon.sh stop resourcemanager
	/opt/hadoop/sbin/mr-jobhistory-daemon.sh stop historyserver
	pdsh -w $$(tr \\n , < slaves) '/opt/hadoop/sbin/hadoop-daemon.sh stop datanode && /opt/hadoop/sbin/yarn-daemon.sh stop nodemanager'
	