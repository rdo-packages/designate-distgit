%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order sphinx openstackdocstheme
%global service designate
%global common_desc Designate is an OpenStack inspired DNSaaS.

Name:           openstack-%{service}
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:          1
Version:        XXX
Release:        XXX
Summary:        OpenStack DNS Service

Group:          Applications/System
License:        Apache-2.0
URL:            http://launchpad.net/%{service}/

Source0:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
Source1:        %{service}.logrotate
Source2:        %{service}-sudoers
Source11:       designate-api.service
Source12:       designate-central.service
Source13:       designate-mdns.service
Source15:       designate-sink.service
Source17:       designate-producer.service
Source18:       designate-worker.service
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  systemd
BuildRequires:  openstack-macros

Requires:       python3-%{service} = %{epoch}:%{version}-%{release}

Requires(pre): shadow-utils

%{?systemd_ordering}

%description
%{common_desc}


%package -n python3-%{service}
Summary:        Designate Python libraries
Group:          Applications/System

Requires:       sudo

%description -n python3-%{service}
%{common_desc}

This package contains the Designate Python library.


%package -n python3-%{service}-tests
Summary:        Designate tests
Group:          Applications/System

Requires:       python3-%{service} = %{epoch}:%{version}-%{release}


%description -n python3-%{service}-tests
%{common_desc}

This package contains Designate test files.


%package common
Summary:        Designate common files
Group:          Applications/System

Requires:       python3-%{service} = %{epoch}:%{version}-%{release}


%description common
%{common_desc}

This package contains Designate files common to all services.


%package agent
Summary:        OpenStack Designate agent
Group:          Applications/System

Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description agent
%{common_desc}

This package contains OpenStack Designate agent.

designate-agent has been removed upstream so this is just an empty package for
backwards compatibility until all the deployment tools removed its installation.


%package api
Summary:        OpenStack Designate API service
Group:          Applications/System

Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description api
%{common_desc}

This package contains OpenStack Designate API service.


%package central
Summary:        OpenStack Designate Central service
Group:          Applications/System

Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description central
%{common_desc}

This package contains OpenStack Designate Central service.


%package mdns
Summary:        OpenStack Designate Mini DNS service
Group:          Applications/System

Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description mdns
%{common_desc}

This package contains OpenStack Designate Mini DNS service.


%package producer
Summary:        OpenStack Designate Producer service
Group:          Applications/System
Obsoletes:      openstack-designate-pool-manager < 9.0.0
Obsoletes:      openstack-designate-zone-manager < 9.0.0

Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description producer
%{common_desc}

This package contains OpenStack Designate Producer service.


%package sink
Summary:        OpenStack Designate Sink service
Group:          Applications/System

Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description sink
%{common_desc}

This package contains OpenStack Designate Sink service.


%package worker
Summary:        OpenStack Designate Worker service
Group:          Applications/System

Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description worker
%{common_desc}

This package contains OpenStack Designate Worker service.


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{service}-%{upstream_version} -S git

find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +



sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%pyproject_wheel

%install
%pyproject_install

# Generate sample config
PYTHONPATH="%{buildroot}/%{python3_sitelib}" oslo-config-generator --config-file=./etc/%{service}/%{service}-config-generator.conf

# Remove unused files
rm -rf %{buildroot}%{python3_sitelib}/bin
rm -rf %{buildroot}%{python3_sitelib}/doc
rm -rf %{buildroot}%{python3_sitelib}/tools

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
install -p -D -m 644 etc/%{service}/%{service}.conf.sample %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf
mv %{buildroot}/usr/etc/%{service}/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}/
mv %{buildroot}/usr/etc/%{service}/rootwrap.conf.sample %{buildroot}%{_sysconfdir}/%{service}/rootwrap.conf
install -d -m 755 %{buildroot}%{_datarootdir}/%{service}/rootwrap
mv %{buildroot}/usr/etc/%{service}/rootwrap.d/*.filters %{buildroot}%{_datarootdir}/%{service}/rootwrap

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{service}

# Install sudoers
install -p -D -m 440 %{SOURCE2} %{buildroot}%{_sysconfdir}/sudoers.d/%{service}

# Install systemd units
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/designate-api.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/designate-central.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/designate-mdns.service
install -p -D -m 644 %{SOURCE15} %{buildroot}%{_unitdir}/designate-sink.service
install -p -D -m 644 %{SOURCE17} %{buildroot}%{_unitdir}/designate-producer.service
install -p -D -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/designate-worker.service

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{service}

%pre common
getent group %{service} >/dev/null || groupadd -r %{service}
getent passwd %{service} >/dev/null || \
    useradd -r -g %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin \
    -c "OpenStack Designate Daemons" %{service}
exit 0


%preun agent
%systemd_preun designate-agent.service


%post api
%systemd_post designate-api.service


%preun api
%systemd_preun designate-api.service


%postun api
%systemd_postun_with_restart designate-api.service


%post central
%systemd_post designate-central.service


%preun central
%systemd_preun designate-central.service


%postun central
%systemd_postun_with_restart designate-central.service


%post mdns
%systemd_post designate-mdns.service


%preun mdns
%systemd_preun designate-mdns.service


%postun mdns
%systemd_postun_with_restart designate-mdns.service


%post producer
%systemd_post designate-producer.service


%preun producer
%systemd_preun designate-producer.service


%postun producer
%systemd_postun_with_restart designate-producer.service


%post sink
%systemd_post designate-sink.service


%preun sink
%systemd_preun designate-sink.service


%postun sink
%systemd_postun_with_restart designate-sink.service


%post worker
%systemd_post designate-worker.service


%preun worker
%systemd_preun designate-worker.service


%postun worker
%systemd_postun_with_restart designate-worker.service


%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{service}/tests


%files -n python3-%{service}
%license LICENSE
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-*.dist-info
%exclude %{python3_sitelib}/%{service}/tests


%files common
%license LICENSE
%doc README.rst
%doc etc/designate/policy.yaml.sample
%dir %{_sysconfdir}/%{service}
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/rootwrap.conf
%dir %{_datarootdir}/%{service}
%dir %{_datarootdir}/%{service}/rootwrap
%{_datarootdir}/%{service}/rootwrap/*.filters
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%config %{_sysconfdir}/sudoers.d/%{service}
%dir %attr(0755, %{service}, %{service}) %{_sharedstatedir}/%{service}
%dir %attr(0750, %{service}, %{service}) %{_localstatedir}/log/%{service}
%{_bindir}/designate-rootwrap
%{_bindir}/designate-manage
%{_bindir}/designate-status
%{_bindir}/designate-api-wsgi


%files agent
%license LICENSE


%files api
%license LICENSE
%{_bindir}/designate-api
%{_unitdir}/designate-api.service
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini


%files central
%license LICENSE
%{_bindir}/designate-central
%{_unitdir}/designate-central.service


%files mdns
%license LICENSE
%{_bindir}/designate-mdns
%{_unitdir}/designate-mdns.service


%files producer
%license LICENSE
%{_bindir}/designate-producer
%{_unitdir}/designate-producer.service


%files sink
%license LICENSE
%{_bindir}/designate-sink
%{_unitdir}/designate-sink.service


%files worker
%license LICENSE
%{_bindir}/designate-worker
%{_unitdir}/designate-worker.service


%changelog
