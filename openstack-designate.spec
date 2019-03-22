%global milestone .0rc1
# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global service designate
%global common_desc Designate is an OpenStack inspired DNSaaS.

Name:           openstack-%{service}
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:          1
Version:        8.0.0
Release:        0.1%{?milestone}%{?dist}
Summary:        OpenStack DNS Service

Group:          Applications/System
License:        ASL 2.0
URL:            http://launchpad.net/%{service}/

Source0:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
#
# patches_base=8.0.0.0rc1
#

Source1:        %{service}.logrotate
Source2:        %{service}-sudoers
Source10:       designate-agent.service
Source11:       designate-api.service
Source12:       designate-central.service
Source13:       designate-mdns.service
Source14:       designate-pool-manager.service
Source15:       designate-sink.service
Source16:       designate-zone-manager.service
Source17:       designate-producer.service
Source18:       designate-worker.service

BuildArch:      noarch

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  systemd
BuildRequires:  openstack-macros
# Required for config file generation
BuildRequires:  python%{pyver}-jsonschema
BuildRequires:  python%{pyver}-keystonemiddleware
BuildRequires:  python%{pyver}-neutronclient
BuildRequires:  python%{pyver}-oslo-concurrency
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-db
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-oslo-messaging
BuildRequires:  python%{pyver}-oslo-middleware
BuildRequires:  python%{pyver}-oslo-policy
BuildRequires:  python%{pyver}-oslo-service
BuildRequires:  python%{pyver}-oslo-upgradecheck
BuildRequires:  python%{pyver}-oslo-versionedobjects
BuildRequires:  python%{pyver}-os-win
BuildRequires:  python%{pyver}-tooz
BuildRequires:  python%{pyver}-dns

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-d2to1
%else
BuildRequires:  python%{pyver}-d2to1
%endif

Requires:       python%{pyver}-%{service} = %{epoch}:%{version}-%{release}

Requires(pre): shadow-utils
%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif

%description
%{common_desc}


%package -n python%{pyver}-%{service}
Summary:        Designate Python libraries
%{?python_provide:%python_provide python%{pyver}-%{service}}
Group:          Applications/System

Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-debtcollector >= 1.2.0
Requires:       python%{pyver}-designateclient >= 2.7.0
Requires:       python%{pyver}-dns >= 1.14.0
Requires:       python%{pyver}-eventlet >= 0.18.2
Requires:       python%{pyver}-greenlet >= 0.4.10
Requires:       python%{pyver}-jinja2 >= 2.10
Requires:       python%{pyver}-jsonschema >= 2.6.0
Requires:       python%{pyver}-keystoneauth1 >= 3.4.0
Requires:       python%{pyver}-keystonemiddleware >= 4.17.0
Requires:       python%{pyver}-netaddr >= 0.7.18
Requires:       python%{pyver}-neutronclient >= 6.7.0
Requires:       python%{pyver}-oslo-concurrency >= 3.26.0
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-context >= 2.19.2
Requires:       python%{pyver}-oslo-db >= 4.27.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-messaging >= 5.29.0
Requires:       python%{pyver}-oslo-middleware >= 3.31.0
Requires:       python%{pyver}-oslo-policy >= 1.30.0
Requires:       python%{pyver}-oslo-reports >= 1.18.0
Requires:       python%{pyver}-oslo-rootwrap >= 5.8.0
Requires:       python%{pyver}-oslo-serialization >= 2.18.0
Requires:       python%{pyver}-oslo-service >= 1.24.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-oslo-upgradecheck >= 0.1.0
Requires:       python%{pyver}-os-win >= 3.0.0
Requires:       python%{pyver}-oslo-versionedobjects >= 1.31.2
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-pecan >= 1.0.0
Requires:       python%{pyver}-requests >= 2.14.2
Requires:       python%{pyver}-tenacity
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-sqlalchemy >= 1.0.10
Requires:       python%{pyver}-stevedore >= 1.20.0
Requires:       python%{pyver}-suds >= 0.6
Requires:       python%{pyver}-tooz >= 1.58.0
Requires:       python%{pyver}-webob >= 1.7.1
Requires:       python%{pyver}-werkzeug >= 0.9
Requires:       python%{pyver}-futurist
Requires:       sudo
# python2-monasca-statsd is in requirements.txt but it's not packaged yet
#Requires:       python%{pyver}-monasca-statsd

# Handle python2 exception
%if %{pyver} == 2
Requires:       python-flask >= 0.10
Requires:       python-memcached >= 1.56
Requires:       python-paste
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-migrate >= 0.11.0
%else
Requires:       python%{pyver}-flask >= 0.10
Requires:       python%{pyver}-memcached >= 1.56
Requires:       python%{pyver}-paste
Requires:       python%{pyver}-paste-deploy >= 1.5.0
Requires:       python%{pyver}-migrate >= 0.11.0
%endif


%description -n python%{pyver}-%{service}
%{common_desc}

This package contains the Designate Python library.


%package -n python%{pyver}-%{service}-tests
Summary:        Designate tests
%{?python_provide:%python_provide python%{pyver}-%{service}-tests}
Group:          Applications/System

Requires:       python%{pyver}-%{service} = %{epoch}:%{version}-%{release}


%description -n python%{pyver}-%{service}-tests
%{common_desc}

This package contains Designate test files.


%package common
Summary:        Designate common files
Group:          Applications/System

Requires:       python%{pyver}-%{service} = %{epoch}:%{version}-%{release}


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

Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description producer
%{common_desc}

This package contains OpenStack Designate Producer service.


%package pool-manager
Summary:        OpenStack Designate Pool Manager service
Group:          Applications/System

Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description pool-manager
%{common_desc}

This package contains OpenStack Designate Pool Manager service.


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


%package zone-manager
Summary:        OpenStack Designate Zone Manager service
Group:          Applications/System

Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description zone-manager
%{common_desc}

This package contains OpenStack Designate Zone Manager service.


%prep
%setup -q -n %{service}-%{upstream_version}

find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# Let's handle dependencies ourselves
%py_req_cleanup


%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{pyver_build}

# Generate sample config
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=./etc/%{service}/%{service}-config-generator.conf

%install
%{pyver_install}

# Remove unused files
rm -rf %{buildroot}%{pyver_sitelib}/bin
rm -rf %{buildroot}%{pyver_sitelib}/doc
rm -rf %{buildroot}%{pyver_sitelib}/tools

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
install -p -D -m 644 etc/%{service}/%{service}.conf %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf
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
install -p -D -m 644 %{SOURCE14} %{buildroot}%{_unitdir}/designate-pool-manager.service
install -p -D -m 644 %{SOURCE15} %{buildroot}%{_unitdir}/designate-sink.service
install -p -D -m 644 %{SOURCE16} %{buildroot}%{_unitdir}/designate-zone-manager.service
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


%post pool-manager
%systemd_post designate-pool-manager.service


%preun pool-manager
%systemd_preun designate-pool-manager.service


%postun pool-manager
%systemd_postun_with_restart designate-pool-manager.service


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


%preun zone-manager
%systemd_preun designate-zone-manager.service


%postun zone-manager
%systemd_postun_with_restart designate-zone-manager.service


%files -n python%{pyver}-%{service}-tests
%license LICENSE
%{pyver_sitelib}/%{service}/tests


%files -n python%{pyver}-%{service}
%license LICENSE
%{pyver_sitelib}/%{service}
%{pyver_sitelib}/%{service}-*.egg-info
%exclude %{pyver_sitelib}/%{service}/tests


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


%files pool-manager
%license LICENSE
%{_bindir}/designate-pool-manager
%{_unitdir}/designate-pool-manager.service


%files sink
%license LICENSE
%{_bindir}/designate-sink
%{_unitdir}/designate-sink.service


%files worker
%license LICENSE
%{_bindir}/designate-worker
%{_unitdir}/designate-worker.service


%files zone-manager
%license LICENSE
%{_bindir}/designate-zone-manager
%{_unitdir}/designate-zone-manager.service


%changelog
* Fri Mar 22 2019 RDO <dev@lists.rdoproject.org> 1:8.0.0-0.1.0rc1
- Update to 8.0.0.0rc1

