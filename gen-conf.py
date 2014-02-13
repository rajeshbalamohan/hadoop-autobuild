import socket
hostname = socket.getfqdn()
from glob import glob

namenode = hostname
resourcemanager = hostname
total_megs=8192

volumes = glob("/grid/[0-9]*/")

def distribute(path):
	return ",".join(["%s/%s" % (v,path) for v in volumes])

core = """
<configuration>

</property>
    <property>
    <name>hadoop.proxyuser.hcat.groups</name>
    <value>*</value>
  </property>
    <property>
    <name>hadoop.proxyuser.hive.groups</name>
    <value>*</value>
  </property>
    <property>
    <name>fs.trash.interval</name>
    <value>360</value>
  </property>
    <property>
    <name>mapreduce.jobtracker.webinterface.trusted</name>
    <value>false</value>
  </property>
    <property>
    <name>io.serializations</name>
    <value>org.apache.hadoop.io.serializer.WritableSerialization</value>
  </property>
    <property>
    <name>fs.checkpoint.size</name>
    <value>0.5</value>
  </property>
    <property>
    <name>hadoop.security.auth_to_local</name>
    <value>
        RULE:[2:$1@$0]([rn]m@.*)s/.*/yarn/
        RULE:[2:$1@$0](jhs@.*)s/.*/mapred/
        RULE:[2:$1@$0]([nd]n@.*)s/.*/hdfs/
        RULE:[2:$1@$0](hm@.*)s/.*/hbase/
        RULE:[2:$1@$0](rs@.*)s/.*/hbase/
        DEFAULT</value>
  </property>
    <property>
    <name>hadoop.security.authorization</name>
    <value>false</value>
  </property>
    <property>
    <name>hadoop.proxyuser.hue.groups</name>
    <value>*</value>
  </property>
    <property>
    <name>hadoop.proxyuser.hue.hosts</name>
    <value>*</value>
  </property>
    <property>
    <name>ipc.client.connection.maxidletime</name>
    <value>30000</value>
  </property>
    <property>
    <name>io.file.buffer.size</name>
    <value>131072</value>
  </property>
    <property>
    <name>hadoop.proxyuser.oozie.hosts</name>
    <value>*</value>
  </property>
    <property>
    <name>io.compression.codecs</name>
    <value>org.apache.hadoop.io.compress.GzipCodec,org.apache.hadoop.io.compress.DefaultCodec</value>
  </property>
    <property>
    <name>ipc.client.idlethreshold</name>
    <value>8000</value>
  </property>
    <property>
    <name>hadoop.proxyuser.hive.hosts</name>
    <value>*</value>
  </property>
    <property>
    <name>hadoop.security.authentication</name>
    <value>simple</value>
  </property>
    <property>
    <name>hadoop.proxyuser.oozie.groups</name>
    <value>*</value>
  </property>
    <property>
    <name>ipc.client.connect.max.retries</name>
    <value>50</value>
  </property>
    <property>
    <name>hadoop.proxyuser.hcat.hosts</name>
    <value>*</value>
  </property>

<property>
  <name>mapreduce.clientfactory.class.name</name>
  <value>org.apache.hadoop.mapred.YarnClientFactory</value>
</property>

 <property>
    <name>yarn.server.principal</name>
    <value>nm/localhost@LOCALHOST</value>
  </property>

<property>
  <name>fs.default.name</name>
  <value>hdfs://%(namenode)s:50070</value>
  <!--
  <value>file:///</value>
  -->
  <description>The name of the default file system.  A URI whose
  scheme and authority determine the FileSystem implementation.  The
  uri's scheme determines the config property (fs.SCHEME.impl) naming
  the FileSystem implementation class.  The uri's authority is used to
  determine the host, port, etc. for a filesystem.</description>
</property>

<property>
  <name>hadoop.tmp.dir</name>
  <value>%(hadoop_tmp)s</value>
  <description>A base for other temporary directories.</description>
</property>
<property>
	<name>dfs.namenode.name.dir</name>
	<value>%(hadoop_name)s</value>
</property>

  <property>
    <name>hadoop.security.authentication</name>
    <!--
    <value>kerberos</value>
    -->
    <value>simple</value>
  </property>

<!--
  <property>
    <name>hadoop.security.authorization</name>
    <value>true</value>
  </property>
-->

 <property>
   <name>hadoop.cluster.administrators</name>
   <value>*</value>
 </property>

<!--
  <property>
    <name>hadoop.security.auth_to_local</name>
    <value>
      DEFAULT
    </value>
  </property>
-->

  <property>
    <name>hadoop.security.auth_to_local</name>
    <value>RULE:[1:$1@$0](.*@localhost)s/@.*//
DEFAULT
</value>
  </property>


  <property>
    <name>dfs.namenode.kerberos.principal</name>
    <!--
    <value>hdfs/localhost@LOCALHOST</value>
    -->
    <value>hdfs/localhost@localhost</value>
  </property>
  <property>
    <name>dfs.datanode.kerberos.principal</name>
    <value>hdfs/localhost@localhost</value>
  </property>
  <property>
    <name>dfs.namenode.keytab.file</name>
    <value>/etc/krb5.keytab</value>
  </property>
  <property>
    <name>dfs.datanode.keytab.file</name>
    <value>/etc/krb5.keytab</value>
  </property> 
  <property>
    <name>dfs.namenode.delegation.key.update-interval</name>
    <value>604800000</value>
  </property>
  <property>
    <name>dfs.namenode.delegation.token.renew-interval</name>
    <value>604800000</value>
  </property>
  <property>
    <name>dfs.namenode.delegation.token.max-lifetime</name>
    <value>604800000</value>
  </property>

  <property>
    <name>dfs.permissions</name>
    <value>true</value>
  </property>

  <property>
    <name>dfs.namenode.kerberos.https.principal</name>
    <value>hdfs/localhost@localhost</value>
  </property>

</configuration>
""" % {'namenode':namenode, 'hadoop_name':distribute('dfs/name'), 'hadoop_tmp':distribute('tmp')}

hdfs = """<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
    <name>dfs.namenode.safemode.threshold-pct</name>
    <value>1.0f</value>
  </property>
    <property>
    <name>dfs.datanode.du.reserved</name>
    <value>1073741824</value>
  </property>
    <property>
    <name>dfs.datanode.max.transfer.threads</name>
    <value>1024</value>
  </property>
    <property>
    <name>dfs.namenode.stale.datanode.interval</name>
    <value>30000</value>
  </property>
    <property>
    <name>dfs.https.port</name>
    <value>50470</value>
  </property>
    <property>
    <name>dfs.cluster.administrators</name>
    <value> hdfs</value>
  </property>
    <property>
    <name>dfs.blockreport.initialDelay</name>
    <value>120</value>
  </property>
    <property>
    <name>dfs.journalnode.http-address</name>
    <value>0.0.0.0:8480</value>
  </property>
    <property>
    <name>dfs.namenode.accesstime.precision</name>
    <value>0</value>
  </property>
    <property>
    <name>dfs.namenode.handler.count</name>
    <value>5</value>
  </property>
    <property>
    <name>dfs.replication</name>
    <value>3</value>
  </property>
    <property>
    <name>dfs.namenode.avoid.write.stale.datanode</name>
    <value>true</value>
  </property>
    <property>
    <name>dfs.permissions.enabled</name>
    <value>false</value>
  </property>
    <property>
    <name>dfs.replication.max</name>
    <value>50</value>
  </property>
    <property>
    <name>fs.permissions.umask-mode</name>
    <value>022</value>
  </property>
    
    <property>
    <name>dfs.namenode.checkpoint.period</name>
    <value>21600</value>
  </property>
    <property>
    <name>dfs.block.access.token.enable</name>
    <value>true</value>
  </property>
    <property>
    <name>dfs.hosts.exclude</name>
    <value>/etc/hadoop/conf/dfs.exclude</value>
  </property>
    <property>
    <name>dfs.namenode.checkpoint.dir</name>
    <value>/hadoop/hdfs/namesecondary</value>
  </property>
    <property>
    <name>dfs.namenode.checkpoint.edits.dir</name>
    <value>${dfs.namenode.checkpoint.dir}</value>
  </property>
    <property>
    <name>dfs.blocksize</name>
    <value>134217728</value>
  </property>
    <property>
    <name>dfs.namenode.http-address</name>
    <value>sandbox.hortonworks.com:50070</value>
  </property>
    <property>
    <name>dfs.namenode.secondary.http-address</name>
    <value>sandbox.hortonworks.com:50090</value>
  </property>
    <property>
    <name>dfs.client.read.shortcircuit.streams.cache.size</name>
    <value>4096</value>
  </property>
  <property>
    <name>dfs.namenode.write.stale.datanode.ratio</name>
    <value>1.0f</value>
  </property>
    <property>
    <name>dfs.support.append</name>
    <value>true</value>
  </property>
    <property>
    <name>dfs.datanode.ipc.address</name>
    <value>0.0.0.0:8010</value>
  </property>
    <property>
    <name>dfs.datanode.balance.bandwidthPerSec</name>
    <value>6250000</value>
  </property>
    <property>
    <name>dfs.heartbeat.interval</name>
    <value>3</value>
  </property>
    <property>
    <name>dfs.datanode.failed.volumes.tolerated</name>
    <value>0</value>
  </property>
    <property>
    <name>dfs.permissions.superusergroup</name>
    <value>hdfs</value>
  </property>
    <property>
    <name>dfs.domain.socket.path</name>
    <value>/var/lib/hadoop-hdfs/dn_socket</value>
  </property>
    <property>
    <name>dfs.namenode.avoid.read.stale.datanode</name>
    <value>true</value>
  </property>
    <property>
    <name>dfs.journalnode.edits.dir</name>
    <value>/grid/0/hdfs/journal</value>
  </property>
    <property>
    <name>dfs.client.read.shortcircuit</name>
    <value>true</value>
  </property>
    <property>
    <name>dfs.client.block.write.replace-datanode-on-failure.policy</name>
    <value>NEVER</value>
  </property>
    <property>
    <name>dfs.webhdfs.enabled</name>
    <value>true</value>
  </property>
    <property>
    <name>dfs.datanode.data.dir.perm</name>
    <value>750</value>
  </property>
   
    <property>
    <name>dfs.namenode.name.dir</name>
    <value>/hadoop/hdfs/namenode</value>
  </property>
    <property>
    <name>dfs.namenode.https-address</name>
    <value>sandbox.hortonworks.com:50470</value>
  </property>



<property>
  <name>dfs.block.local-path-access.user</name>
  <value>root</value>
</property>

<property>
  <name>hadoop.tmp.dir</name>
  <value>%(hadoop_tmp)s</value>
  <description>A base for other temporary directories.</description>
</property>

<property>
  <name>dfs.http.address</name>
  <value>%(namenode)s:50070</value>
  <description>
    The address and the base port where the dfs namenode web ui will listen on.
    If the port is 0 then the server will start on a free port.
  </description>
</property>

<property>
  <name>dfs.https.port</name>
  <value>0</value>
  <description>
    The address and the base port where the dfs namenode web ui will listen on.
    If the port is 0 then the server will start on a free port.
  </description>
</property>

<property>
  <name>dfs.datanode.failed.volumes.tolerated</name>
  <value>0</value>
  <description>The number of volumes that are allowed to
  fail before a datanode stops offering service. By default
  any volume failure will cause a datanode to shutdown.
  </description>
</property>

<property>
<name>dfs.datanode.data.dir</name>
<value>%(hadoop_data)s</value>
</property>

<property>
  <name>dfs.datanode.address</name>
  <value>0.0.0.0:50010</value>
  <description>
    The address where the datanode server will listen to.
    If the port is 0 then the server will start on a free port.
  </description>
</property>

<property>
  <name>dfs.datanode.http.address</name>
  <value>0.0.0.0:50011</value>
  <description>
    The datanode http server address and port.
    If the port is 0 then the server will start on a free port.
  </description>
</property>

</configuration>
""" % {'namenode' : namenode, 'hadoop_tmp' : distribute('tmp'), 'hadoop_data' : distribute('dfs/data')}

yarn = """<?xml version="1.0"?>
<configuration>

  <property>
    <name>yarn.nodemanager.remote-app-log-dir</name>
    <value>/app-logs</value>
  </property>
    <property>
    <name>yarn.nodemanager.local-dirs</name>
    <value>/hadoop/yarn/local</value>
  </property>
    <property>
    <name>yarn.nodemanager.container-executor.class</name>
    <value>org.apache.hadoop.yarn.server.nodemanager.DefaultContainerExecutor</value>
  </property>
    <property>
    <name>yarn.nodemanager.health-checker.interval-ms</name>
    <value>135000</value>
  </property>
    <property>
    <name>yarn.nodemanager.admin-env</name>
    <value>MALLOC_ARENA_MAX=$MALLOC_ARENA_MAX</value>
  </property>
    <property>
    <name>yarn.application.classpath</name>
    <value>/etc/hadoop/conf,/usr/lib/hadoop/*,/usr/lib/hadoop/lib/*,/usr/lib/hadoop-hdfs/*,/usr/lib/hadoop-hdfs/lib/*,/usr/lib/hadoop-yarn/*,/usr/lib/hadoop-yarn/lib/*,/usr/lib/hadoop-mapreduce/*,/usr/lib/hadoop-mapreduce/lib/*</value>
  </property>
    <property>
    <name>yarn.nodemanager.linux-container-executor.group</name>
    <value>hadoop</value>
  </property>
    

    <property>
    <name>yarn.nodemanager.aux-services.mapreduce_shuffle.class</name>
    <value>org.apache.hadoop.mapred.ShuffleHandler</value>
  </property>
    <property>
    <name>yarn.resourcemanager.scheduler.class</name>
    <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler</value>
  </property>
    <property>
    <name>yarn.resourcemanager.am.max-attempts</name>
    <value>2</value>
  </property>
  
    <property>
    <name>yarn.nodemanager.delete.debug-delay-sec</name>
    <value>0</value>
  </property>
    <property>
    <name>yarn.nodemanager.vmem-check-enabled</name>
    <value>false</value>
  </property>
    <property>
    <name>yarn.resourcemanager.hostname</name>
    <value>sandbox.hortonworks.com</value>
  </property>
    <property>
    <name>yarn.acl.enable</name>
    <value>true</value>
  </property>
  
    <property>
    <name>yarn.nodemanager.remote-app-log-dir-suffix</name>
    <value>logs</value>
  </property>
    <property>
    <name>yarn.scheduler.minimum-allocation-mb</name>
    <value>64</value>
  </property>
    <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
    <property>
    <name>yarn.nodemanager.log-dirs</name>
    <value>/hadoop/yarn/log</value>
  </property>
    <property>
    <name>yarn.log-aggregation.retain-seconds</name>
    <value>2592000</value>
  </property>
    <property>
    <name>yarn.nodemanager.log.retain-second</name>
    <value>604800</value>
  </property>
   
    <property>
    <name>yarn.nodemanager.disk-health-checker.min-healthy-disks</name>
    <value>0.25</value>
  </property>
    <property>
    <name>yarn.nodemanager.health-checker.script.timeout-ms</name>
    <value>60000</value>
  </property>
    <property>
    <name>yarn.scheduler.maximum-allocation-mb</name>
    <value>2048</value>
  </property>
    
    <property>
    <name>yarn.nodemanager.resource.memory-mb</name>
    <value>2250</value>
  </property>
    <property>
    <name>yarn.log-aggregation-enable</name>
    <value>true</value>
  </property>
    <property>
    <name>yarn.nodemanager.container-monitor.interval-ms</name>
    <value>3000</value>
  </property>
    
    <property>
    <name>yarn.nodemanager.log-aggregation.compression-type</name>
    <value>gz</value>
  </property>
    <property>
    <name>yarn.nodemanager.vmem-pmem-ratio</name>
    <value>10</value>
  </property>
    <property>
    <name>yarn.admin.acl</name>
    <value>*</value>
  </property>

 <property>
    <name>yarn.resourcemanager.admin.acl</name>
    <value>false</value>
  </property>

 <property>
    <name>yarn.resourcemanager.am.max-retries</name>
    <value>4</value>
  </property>

  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>

  <property>
    <name>yarn.nodemanager.aux-services.shuffle.class</name>
    <value>org.apache.hadoop.mapred.ShuffleHandler</value>
  </property>

  <property>
    <name>mapreduce.jobhistory.keytab</name>
    <value>/etc/krb5.keytab</value>
  </property>

  <property>
    <name>mapreduce.jobhistory.principal</name>
    <value>rm/localhost@localhost.eglbp.corp.yahoo.com</value>
  </property>


<!-- All resourcemanager related configuration properties -->
  <property>
    <name>yarn.resourcemanager.address</name>
    <value>%(resourcemanager)s:8032</value>
  </property>

  <property>
    <name>yarn.resourcemanager.resource-tracker.address</name>
    <value>%(resourcemanager)s:8031</value>
  </property>

  <property>
    <name>yarn.resourcemanager.scheduler.address</name>
    <value>%(resourcemanager)s:8030</value>
  </property>

  <property>
    <name>yarn.resourcemanager.nodes.exclude-path</name>
    <value>/opt/hadoop/etc/hadoop/excluded-nodes</value>
  </property>


<!--
  <property>
     <name>yarn.resourcemanager.webapp.address</name>
     <value>localhost:8088</value>
  </property>
-->

<!--
  <property>
    <name>yarn.resourcemanager.scheduler.class</name>
    <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler</value>
  </property>
-->
 
  <property>
    <name>yarn.server.resourcemanager.application.expiry.interval</name>
    <value>60000</value>
  </property>

  <property>
    <name>yarn.server.resourcemanager.keytab</name>
    <value>/etc/krb5.keytab</value>
  </property>

<!-- All nodemanager related configuration properties -->

  <property>
    <name>yarn.nodemanager.local-dirs</name>
    <value>%(hadoop_nm_local)s</value>
  </property>

  <property>
    <name>yarn.nodemanager.log-dirs</name>
    <value>%(hadoop_nm_log)s</value>
  </property>

  <property>
    <name>yarn.server.nodemanager.remote-app-log-dir</name>
   <!--
   <value>/tmp/test-logs</value>
   -->
   <value>/app-logs</value>
  </property>

  <property>
    <name>yarn.log-aggregation-enable</name>
    <value>true</value>
  </property>

  <property>
    <name>yarn.server.nodemanager.keytab</name>
    <value>/etc/krb5.keytab</value>
  </property>

  <property>
    <name>yarn.nodemanager.container-executor.class</name>
    <value>org.apache.hadoop.yarn.server.nodemanager.DefaultContainerExecutor</value>
    <!--
    <value>org.apache.hadoop.yarn.server.nodemanager.LinuxContainerExecutor</value>
    -->
  </property>

  <property>
    <name>yarn.server.nodemanager.address</name>
    <value>0.0.0.0:45454</value>
  </property>

  <!--<property>
    <name>yarn.nodemanager.health-checker.script.path</name>
    <value>/Users/vinodkv/tmp/conf/healthCheckerNotExisting</value>
    <description>Location of the node's health-check script on the local
    file-system.
    </description>
  </property>-->

  <property>
    <name>yarn.nodemanager.health-checker.interval-ms</name>
    <value>5000</value>
    <description>Frequency of the health-check run by the NodeManager
    </description>
  </property>

  <property>
    <name>yarn.server.nodemanager.healthchecker.script.timeout</name>
    <value>120000</value>
    <description>Timeout for the health-check run by the NodeManager
    </description>
  </property>

  <property>
    <name>yarn.server.nodemanager.healthchecker.script.args</name>
    <value></value>
    <description>Arguments to be passed to the health-check script run
    by the NodeManager</description>
  </property>

  <property>
    <name>yarn.server.nodemanager.containers-monitor.monitoring-interval</name>
    <value>3000</value>
  </property>

  <property>
    <name>yarn.server.nodemanager.containers-monitor.resourcecalculatorplugin</name>
    <value>org.apache.hadoop.yarn.util.LinuxResourceCalculatorPlugin</value>
    <final>true</final>
  </property>

   <property>
     <name>yarn.server.nodemanager.reserved-physical-memory.mb</name>
     <value>-1</value>
   </property>

<!-- All MRAppManager related configuration properties -->

  <property>
    <name>yarn.server.mapreduce-appmanager.attempt-listener.bindAddress</name>
    <value>0.0.0.0</value>
  </property>

  <property>
    <name>yarn.server.mapreduce-appmanager.client-service.bindAddress</name>
    <value>0.0.0.0</value>
  </property>

  <property>
    <name>yarn.nodemanager.resource.memory-mb</name>
    <value>12288</value>
  </property>

  <property>
    <name>yarn.nodemanager.vmem-pmem-ratio</name>
    <value>20.0</value>
  </property>


  <property>
   <name>mapreduce.job.hdfs-servers</name>
   <value>${fs.default.name}</value>
 </property>

 <property>
   <name>yarn.server.nodemanager.jobhistory</name>
    <!-- cluster variant -->
    <value>/tmp/yarn/done</value>
    <description>The name of the default file system.  Either the
  literal string "local" or a host:port for NDFS.</description>
    <final>true</final>
  </property>

<property>
	<name>yarn.nodemanager.process-kill-wait.ms</name>
	<value>3600000</value>
</property>

<property>
	<name>yarn.nodemanager.sleep-delay-before-sigkill.ms</name>
	<value>3600000</value>
</property>

<property>
	<name>yarn.nodemanager.resource.memory-mb</name>
	<value>%(total_megs)d</value>
</property>

</configuration>
""" % {'resourcemanager' : resourcemanager, 'hadoop_tmp':distribute('tmp'), 'hadoop_nm_local':distribute('tmp/nm-local'), 'hadoop_nm_log':distribute('tmp/nm-logs'), 'total_megs': total_megs}

mapred = """<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>


  <property>
    <name>yarn.app.mapreduce.am.resource.mb</name>
    <value>250</value>
  </property>
    <property>
    <name>mapreduce.cluster.administrators</name>
    <value>hadoop</value>
  </property>
    <property>
    <name>mapreduce.map.java.opts</name>
     <value>-Xmx512m -Djava.net.preferIPv4Stack=true -XX:+UseNUMA -XX:NewRatio=12 -XX:MaxHeapFreeRatio=40 -XX:MinHeapFreeRatio=15 </value>
  </property>
  <property>
    <name>mapred.child.java.opts</name>
    <value>-server -Xmx1200m -XX:+UseParallelGC -XX:NewRatio=8 -Djava.net.preferIPv4Stack=true</value>
    </property>
  <property>
    <name>mapreduce.reduce.shuffle.parallelcopies</name>
    <value>30</value>
  </property>
    <property>
    <name>mapreduce.task.io.sort.factor</name>
    <value>100</value>
  </property>
    <property>
    <name>yarn.app.mapreduce.am.admin-command-opts</name>
    <value>-Djava.net.preferIPv4Stack=true -Dhadoop.metrics.log.level=WARN</value>
  </property>
    <property>
    <name>mapreduce.admin.reduce.child.java.opts</name>
    <value>-Djava.net.preferIPv4Stack=true -Dhadoop.metrics.log.level=WARN</value>
  </property>
    <property>
    <name>mapreduce.application.classpath</name>
    <value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*,$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
  </property>
    <property>
    <name>yarn.app.mapreduce.am.log.level</name>
    <value>INFO</value>
  </property>
    <property>
    <name>mapreduce.jobhistory.webapp.address</name>
    <value>sandbox.hortonworks.com:19888</value>
  </property>
    <property>
    <name>mapreduce.reduce.input.buffer.percent</name>
    <value>0.0</value>
  </property>
    <property>
    <name>mapreduce.reduce.java.opts</name>
    <value>-Xmx512m -Djava.net.preferIPv4Stack=true -XX:+UseNUMA -XX:NewRatio=12 -XX:MaxHeapFreeRatio=40 -XX:MinHeapFreeRatio=15 </value>
  </property>
    <property>
    <name>mapreduce.admin.map.child.java.opts</name>
    <value>-Djava.net.preferIPv4Stack=true -Dhadoop.metrics.log.level=WARN</value>
  </property>
    <property>
    <name>yarn.app.mapreduce.am.command-opts</name>
    <value>-Xmx312m</value>
  </property>
    <property>
    <name>mapreduce.reduce.memory.mb</name>
    <value>512</value>
  </property>
    <property>
    <name>mapreduce.task.io.sort.mb</name>
    <value>200</value>
  </property>
    <property>
    <name>mapreduce.output.fileoutputformat.compress.type</name>
    <value>BLOCK</value>
  </property>
    <property>
    <name>mapreduce.jobhistory.address</name>
    <value>sandbox.hortonworks.com:10020</value>
  </property>
    <property>
    <name>mapreduce.reduce.log.level</name>
    <value>INFO</value>
  </property>
    <property>
    <name>mapreduce.jobhistory.done-dir</name>
    <value>/mr-history/done</value>
  </property>
    <property>
    <name>mapreduce.admin.user.env</name>
    <value>LD_LIBRARY_PATH=/usr/lib/hadoop/lib/native:/usr/lib/hadoop/lib/native/`$JAVA_HOME/bin/java -d32 -version &amp;&gt; /dev/null;if [ $? -eq 0 ]; then echo Linux-i386-32; else echo Linux-amd64-64;fi`</value>
  </property>
    <property>
    <name>mapreduce.map.memory.mb</name>
    <value>512</value>
  </property>
    <property>
    <name>mapreduce.reduce.speculative</name>
    <value>false</value>
  </property>
    <property>
    <name>mapreduce.output.fileoutputformat.compress</name>
    <value>false</value>
  </property>
    <property>
    <name>mapreduce.reduce.shuffle.input.buffer.percent</name>
    <value>0.7</value>
  </property>
    <property>
    <name>mapreduce.am.max-attempts</name>
    <value>2</value>
  </property>
    <property>
    <name>mapreduce.map.output.compress</name>
    <value>false</value>
  </property>
    <property>
    <name>mapreduce.reduce.shuffle.merge.percent</name>
    <value>0.66</value>
  </property>
    <property>
    <name>mapreduce.map.log.level</name>
    <value>INFO</value>
  </property>
    <property>
    <name>yarn.app.mapreduce.am.staging-dir</name>
    <value>/user</value>
  </property>
    <property>
    <name>mapreduce.jobhistory.intermediate-done-dir</name>
    <value>/mr-history/tmp</value>
  </property>
    <property>
    <name>mapreduce.map.speculative</name>
    <value>false</value>
  </property>
    <property>
    <name>mapreduce.shuffle.port</name>
    <value>13562</value>
  </property>
    <property>
    <name>mapreduce.framework.name</name>
    <value>yarn-tez</value>
  </property>
    <property>
    <name>mapreduce.job.reduce.slowstart.completedmaps</name>
    <value>0.05</value>
  </property>
    <property>
    <name>mapreduce.map.sort.spill.percent</name>
    <value>0.7</value>
  </property>
    <property>
    <name>mapreduce.task.timeout</name>
    <value>300000</value>
  </property>

<!-- Put site-specific property overrides in this file. -->

<configuration>

<property>
  <name>mapreduce.jobhistory.address</name>
  <value>%(jhs)s:10020</value>
</property>

<property>
  <name>mapred.job.tracker.history.completed.location</name>
  <value>/history/done/</value>
  <description> The completed job history files are stored at this single well 
  known location. If nothing is specified, the files are stored at 
  ${hadoop.job.history.location}/done.
  </description>
</property>

<property>
<name>mapreduce.history.server.http.address</name>
<value>%(jhs)s:63678</value>
</property>

<property>
<name>mapreduce.history.server.embedded</name>
<value>false</value>
<value>%(jhs)s:65678</value>
</property>

<property>
<name>mapreduce.history.server.embedded</name>
<value>false</value>
</property>

<property>
  <name>webinterface.private.actions</name>
  <value>true</value>
  <description> If set to true, the web interfaces of JT and NN may contain 
                actions, such as kill job, delete file, etc., that should 
                not be exposed to public. Enable this option if the interfaces 
                are only reachable by those who have the right authorization.
  </description>
</property>


<property>
  <name>mapred.jobtracker.taskScheduler</name>
 <value>org.apache.hadoop.mapred.JobQueueTaskScheduler</value>
  <description>The class responsible for scheduling the tasks.</description>
</property>


<property>
  <name>mapred.jobtracker.completeuserjobs.maximum</name>
  <value>1</value>
  <description>The maximum number of complete jobs per user to keep around 
  before delegating them to the job history.</description>
</property>

<property>
<name>mapred.local.dir</name>
<value>/tmp/mapred-local/0_0,/tmp/mapred-local/0_1,/tmp/mapred-local/0_2,/tmp/mapred-local/0_3</value>
</property>
<property>
  <name>mapred.job.reuse.jvm.num.tasks</name>
  <value>-1</value>
  <description>How many tasks to run per jvm. If set to -1, there is
  no limit. 
  </description>
</property>

<property>
  <name>mapred.task.tracker.report.address</name>
  <value>127.0.0.1:0</value>
  <description>The interface and port that task tracker server listens on. 
  Since it is only connected to by the tasks, it uses the local interface.
  EXPERT ONLY. Should only be changed if your host does not have the loopback 
  interface.</description>
</property>

<property>
  <name>mapred.task.tracker.http.address</name>
  <value>0.0.0.0:0</value>
  <description>
    The task tracker http server address and port.
    If the port is 0 then the server will start on a free port.
  </description>
</property>

<property>
  <name>mapred.tasktracker.map.tasks.maximum</name>
  <value>2</value>
  <description>The maximum number of map tasks that will be run
  simultaneously by a task tracker.
  </description>
</property>

<property>
  <name>mapred.tasktracker.reduce.tasks.maximum</name>
  <value>2</value>
  <description>The maximum number of reduce tasks that will be run
  simultaneously by a task tracker.
  </description>
</property>

<!--
<property>
<name>mapred.cluster.map.memory.mb</name>
<value>1024</value>
</property>

<property>
<name>mapred.cluster.reduce.memory.mb</name>
<value>2048</value>
</property>


<property>
<name>mapred.job.map.memory.mb</name>
<value>1024</value>
</property>

<property>
<name>mapred.job.reduce.memory.mb</name>
<value>2048</value>
</property>


<property>
<name>mapred.cluster.max.map.memory.mb</name>
<value>2048</value>
</property>

<property>
<name>mapred.cluster.max.reduce.memory.mb</name>
<value>4096</value>
</property>
-->
<property>
<name>mapreduce.cluster.map.userlog.retain-size</name>
<value>1024</value>
</property>

<property>
<name>mapreduce.cluster.reduce.userlog.retain-size</name>
<value>1024</value>
</property>

<property>
  <name>mapred.tasktracker.taskmemorymanager.monitoring-interval</name>
  <value>1000</value>
  <description>The interval, in milliseconds, for which the tasktracker waits
   between two cycles of monitoring its tasks' memory usage. Used only if
   tasks' memory management is enabled via mapred.tasktracker.tasks.maxmemory.
   </description>
</property>

<property>
<name>mapred.map.task.debug.script</name>
<value></value>
<final>true</final>
</property>

<property>
  <name>mapred.job.queue.name</name>
  <value>default</value>
</property>

<property>
  <name>mapred.child.java.opts</name>
  <value>-Xmx1024m<!--yourkit:-agentpath:/opt/yourkit/bin/linux-x86-64/libyjpagent.so=dir=/grid/0/yjp,filters=/dev/null,tracing,disablej2ee--></value> 
</property>

<property>
  <name>mapreduce.job.counters.limit</name>
  <value>1024</value>
</property>

</configuration>
""" % ({'jhs':hostname})

open("core-site.xml", "w").write(core)
open("hdfs-site.xml", "w").write(hdfs)
open("yarn-site.xml", "w").write(yarn)
open("mapred-site.xml", "w").write(mapred)
