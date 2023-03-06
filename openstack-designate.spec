%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
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
License:        ASL 2.0
URL:            http://launchpad.net/%{service}/

Source0:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
Source1:        %{service}.logrotate
Source2:        %{service}-sudoers
Source10:       designate-agent.service
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
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  systemd
BuildRequires:  openstack-macros
# Required for config file generation
BuildRequires:  python3-jsonschema
BuildRequires:  python3-keystonemiddleware
BuildRequires:  python3-neutronclient
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-db
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-messaging
BuildRequires:  python3-oslo-middleware
BuildRequires:  python3-oslo-policy
BuildRequires:  python3-oslo-service
BuildRequires:  python3-oslo-upgradecheck
BuildRequires:  python3-oslo-versionedobjects
BuildRequires:  python3-os-win
BuildRequires:  python3-tooz
BuildRequires:  python3-dns

Requires:       python3-%{service} = %{epoch}:%{version}-%{release}

Requires(pre): shadow-utils
%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif

%description
%{common_desc}


%package -n python3-%{service}
Summary:        Designate Python libraries
%{?python_provide:%python_provide python3-%{service}}
Group:          Applications/System

Requires:       python3-debtcollector >= 1.19.0
Requires:       python3-designateclient >= 2.12.0
Requires:       python3-dns >= 2.2.1
Requires:       python3-eventlet >= 0.26.1
Requires:       python3-greenlet >= 0.4.15
Requires:       python3-jinja2 >= 2.10
Requires:       python3-jsonschema >= 3.2.0
Requires:       python3-keystoneauth1 >= 3.4.0
Requires:       python3-keystonemiddleware >= 4.17.0
Requires:       python3-neutronclient >= 6.7.0
Requires:       python3-oslo-concurrency >= 4.2.0
Requires:       python3-oslo-config >= 2:6.8.0
Requires:       python3-oslo-context >= 4.0.0
Requires:       python3-oslo-db >= 8.3.0
Requires:       python3-oslo-i18n >= 3.20.0
Requires:       python3-oslo-log >= 4.3.0
Requires:       python3-oslo-messaging >= 14.1.0
Requires:       python3-oslo-middleware >= 3.31.0
Requires:       python3-oslo-policy >= 3.7.0
Requires:       python3-oslo-reports >= 1.18.0
Requires:       python3-oslo-rootwrap >= 5.15.0
Requires:       python3-oslo-serialization >= 2.25.0
Requires:       python3-oslo-service >= 1.31.0
Requires:       python3-oslo-utils >= 4.7.0
Requires:       python3-oslo-upgradecheck >= 1.3.0
Requires:       python3-os-win >= 4.1.0
Requires:       python3-oslo-versionedobjects >= 1.31.2
Requires:       python3-pbr >= 3.1.1
Requires:       python3-pecan >= 1.0.0
Requires:       python3-requests >= 2.23.0
Requires:       python3-tenacity >= 6.0.0
Requires:       python3-sqlalchemy >= 1.2.19
Requires:       python3-stevedore >= 1.20.0
Requires:       python3-tooz >= 1.58.0
Requires:       python3-webob >= 1.7.1
Requires:       python3-futurist >= 1.2.0
Requires:       python3-edgegrid >= 1.1.1
Requires:       sudo

Requires:       python3-flask >= 2.2.1
Requires:       python3-memcached >= 1.56
Requires:       python3-paste >= 2.0.2
Requires:       python3-paste-deploy >= 1.5.0
Requires:       python3-alembic >= 1.8.0
Requires:       python3-osprofiler >= 3.4.0

%description -n python3-%{service}
%{common_desc}

This package contains the Designate Python library.


%package -n python3-%{service}-tests
Summary:        Designate tests
%{?python_provide:%python_provide python3-%{service}-tests}
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
%setup -q -n %{service}-%{upstream_version}

find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# Let's handle dependencies ourselves
%py_req_cleanup


%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{py3_build}

# Generate sample config
PYTHONPATH=. oslo-config-generator --config-file=./etc/%{service}/%{service}-config-generator.conf

%install
%{py3_install}

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
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/designate-agent.service
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


%post agent
%systemd_post designate-agent.service


%preun agent
%systemd_preun designate-agent.service


%postun agent
%systemd_postun_with_restart designate-agent.service


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
%{python3_sitelib}/%{service}-*.egg-info
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
%{_bindir}/designate-agent
%{_unitdir}/designate-agent.service


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
