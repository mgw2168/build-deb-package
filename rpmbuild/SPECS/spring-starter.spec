##### HEADER SECTION #####

Name:           spring-starter
Version:        0.1.0
Release:        0
Summary:        Rpm package for Spring Starter

License:        ASL 2.0
URL:            https://spring.io
Source0:        gs-spring-boot-：:%{version}.jar
Source1:				%{name}.service

Requires:       shadow-utils,bash
BuildRequires:	systemd
%{?systemd_requires}

BuildArch:      noarch

%description
%{summary}

# disable debuginfo, which is useless on binary-only packages
%define debug_package %{nil}

# do not repack jar files
%define __jar_repack %{nil}

##### PREPARATION SECTION #####
%prep

# empty section

##### BUILD SECTION #####
%build

# empty section

##### PREINSTALL SECTION #####
%pre

# create Spring Starter service group
getent group spring-starter >/dev/null || groupadd -f -g 30000 -r spring-starter

# create Spring Starter service user
if ! getent passwd spring-starter >/dev/null ; then
    if ! getent passwd 30000 >/dev/null ; then
      useradd -r -u 30000 -g spring-starter -d /home/spring-starter -s /sbin/nologin -c "Spring Starter service account" spring-starter
    else
      useradd -r -g spring-starter -d /home/spring-starter -s /sbin/nologin -c "Spring Starter service account" spring-starter
    fi
fi
exit 0

##### INSTALL SECTION #####
%install

app_dir=%{buildroot}/usr/local/spring-starter
data_dir=%{buildroot}/var/opt/spring-starter
service_dir=%{buildroot}/%{_unitdir}

# cleanup build root
rm -rf %{buildroot}
mkdir -p  %{buildroot}

# create app folder
mkdir -p $app_dir

# create data folder
mkdir -p $data_dir

# create service folder
mkdir -p $service_dir

# copy all files
cp %{SOURCE0} $app_dir/gs-spring-boot.jar
cp %{SOURCE1} $service_dir

##### FILES SECTION #####
%files

# define default file attributes
%defattr(-,spring-starter,spring-starter,-)

# list of directories that are packaged
%dir /usr/local/spring-starter
%dir %attr(660, -, -) /var/opt/spring-starter

# list of files that are packaged
/usr/local/spring-starter/gs-spring-boot.jar
/usr/lib/systemd/system/%{name}.service

##### POST INSTALL SECTION #####
%post

# ensure Spring Starter service is enabled and running
%systemd_post %{name}.service
%{_bindir}/systemctl enable %{name}.service
%{_bindir}/systemctl start %{name}.service

##### UNINSTALL SECTION #####
%preun

# ensure Spring Starter service is disabled and stopped
%systemd_preun %{name}.service

%postun

case "$1" in
	0) # This is a package remove

		# remove app and data folders
		rm -rf /usr/local/spring-starter
		rm -rf /var/opt/spring-starter

		# remove Spring Starter service user and group
		userdel spring-starter
	;;
	1) # This is a package upgrade
		# do nothing
	;;
esac

# ensure Spring Starter service restartet if an upgrade is performed
%systemd_postun_with_restart %{name}.service

##### CHANGELOG SECTION #####
%changelog

* Thu Nov 03 2022 Janik vonRotz <contact@janikvonrotz.ch> - 0.1.0-0
- First spring-starter package

