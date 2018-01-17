#!/bin/sh
#
# Install and configure Oracle JDK 8 for Ubuntu/Debian. If JDK was already
# installed with this script then it will be replaced.
#
# Steven P. Goldsmith
# sgjava@gmail.com
# 

# Get start time
dateformat="+%a %b %-eth %Y %I:%M:%S %p %Z"
starttime=$(date "$dateformat")
starttimesec=$(date +%s)

# Get current directory
curdir=$(cd `dirname $0` && pwd)

# Get architecture
arch=$(uname -m)

# Temp dir for downloads, etc.
tmpdir="$HOME/temp"

# JDK archive stuff
javahome=/usr/lib/jvm/jdk1.8.0
jdkurl="http://download.oracle.com/otn-pub/java/jdk/8u162-b12/0da788060d494f5095bf8624735fa2f1/"
jdkver="jdk1.8.0_162"
# ARM 32
if [ "$arch" = "armv7l" ]; then
	jdkarchive="jdk-8u162-linux-arm32-vfp-hflt.tar.gz"
	jnaplatform="https://github.com/java-native-access/jna/raw/master/lib/native/linux-arm.jar"
# ARM 64
elif [ "$arch" = "aarch64" ]; then
	jdkarchive="jdk-8u162-linux-arm64-vfp-hflt.tar.gz"
	jnaplatform="https://github.com/java-native-access/jna/raw/master/lib/native/linux-arm.jar"
# X86
elif [ "$arch" = "i586" ] || [ "$arch" = "i686" ]; then
	jdkarchive="jdk-8u162-linux-i586.tar.gz"
	jnaplatform="https://github.com/java-native-access/jna/raw/master/lib/native/linux-x86.jar"
# X86_64	
elif [ "$arch" = "x86_64" ]; then
	jdkarchive="jdk-8u162-linux-x64.tar.gz"
	jnaplatform="https://github.com/java-native-access/jna/raw/master/lib/native/linux-x86-64.jar"
fi

# JNA jar (4.5.1 causes UnsatisfiedLinkError)
jnajar="central.maven.org/maven2/net/java/dev/jna/jna/4.5.0/jna-4.5.0.jar"

# stdout and stderr for commands logged
logfile="$curdir/install-java.log"
rm -f $logfile

# Simple logger
log(){
	timestamp=$(date +"%m-%d-%Y %k:%M:%S")
	echo "$timestamp $1"
	echo "$timestamp $1" >> $logfile 2>&1
}

log "Installing Java..."

# Remove temp dir
log "Removing temp dir $tmpdir"
rm -rf "$tmpdir" >> $logfile 2>&1
mkdir -p "$tmpdir" >> $logfile 2>&1

# Install Oracle Java JDK
echo -n "Downloading $jdkarchive to $tmpdir     "
wget --directory-prefix=$tmpdir --timestamping --progress=dot --no-cookies --no-check-certificate --header "Cookie: oraclelicense=accept-securebackup-cookie" "$jdkurl$jdkarchive" 2>&1 | grep --line-buffered "%" |  sed -u -e "s,\.,,g" | awk '{printf("\b\b\b\b%4s", $2)}'
echo
log "Extracting $jdkarchive to $tmpdir"
tar -xf "$tmpdir/$jdkarchive" -C "$tmpdir" >> $logfile 2>&1
log "Removing $javahome"
rm -rf "$javahome" >> $logfile 2>&1
mkdir -p /usr/lib/jvm >> $logfile 2>&1
log "Moving $tmpdir/$jdkver to $javahome"
mv "$tmpdir/$jdkver" "$javahome" >> $logfile 2>&1
update-alternatives --quiet --install "/usr/bin/java" "java" "$javahome/bin/java" 1 >> $logfile 2>&1
update-alternatives --quiet --install "/usr/bin/javac" "javac" "$javahome/bin/javac" 1 >> $logfile 2>&1
# See if JAVA_HOME exists and if not add it to /etc/environment
if grep -q "JAVA_HOME" /etc/environment; then
	log "JAVA_HOME already exists"
else
	# Add JAVA_HOME to /etc/environment
	log "Adding JAVA_HOME to /etc/environment"
	echo "JAVA_HOME=$javahome" >> /etc/environment
	. /etc/environment
	log "JAVA_HOME = $JAVA_HOME"
fi

log "Downloading JNA jars..."
rm -f jna*.jar linux*.jar
wget $jnajar
wget $jnaplatform
$javahome/bin/jar xf $(basename "$jnaplatform") libjnidispatch.so
chmod a+x libjnidispatch.so
sudo mv libjnidispatch.so /usr/local/lib

# Clean up
log "Removing $tmpdir"
rm -rf "$tmpdir" 

# Get end time
endtime=$(date "$dateformat")
endtimesec=$(date +%s)

# Show elapsed time
elapsedtimesec=$(expr $endtimesec - $starttimesec)
ds=$((elapsedtimesec % 60))
dm=$(((elapsedtimesec / 60) % 60))
dh=$((elapsedtimesec / 3600))
displaytime=$(printf "%02d:%02d:%02d" $dh $dm $ds)
log "Elapsed time: $displaytime"

