%define milestone .0rc1
%global service designate
%global common_desc Designate is an OpenStack inspired DNSaaS.


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-%{service}
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:          1
Version:        2.0.0
Release:        0.1%{?milestone}%{?dist}
Summary:        OpenStack DNS Service

Group:          Applications/System
License:        ASL 2.0
URL:            http://launchpad.net/%{service}/

Source0:        http://tarballs.openstack.org/%{service}/%{service}-%{version}%{?milestone}.tar.gz
Source1:        %{service}.logrotate
Source2:        %{service}-sudoers
Source10:       designate-agent.service
Source11:       designate-api.service
Source12:       designate-central.service
Source13:       designate-mdns.service
Source14:       designate-pool-manager.service
Source15:       designate-sink.service
Source16:       designate-zone-manager.service

Source30:       %{service}-dist.conf

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-d2to1
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  systemd-units

Requires:       python-%{service} = %{epoch}:%{version}-%{release}
Requires:       openstack-utils

Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd


%description
%{common_desc}


%package -n python-%{service}
Summary:        Designate Python libraries
Group:          Applications/System

Requires:       python-babel >= 1.3
Requires:       python-dns >= 1.12.0
Requires:       python-eventlet >= 0.16.1
Requires:       python-flask >= 0.10
Requires:       python-greenlet >= 0.3.2
Requires:       python-iso8601 >= 0.1.9
Requires:       python-jinja2 >= 2.6
Requires:       python-jsonschema >= 2.0.0
Requires:       python-keystonemiddleware >= 1.5.0
Requires:       python-memcached >= 1.48
Requires:       python-migrate >= 0.9.5
Requires:       python-netaddr >= 0.7.12
Requires:       python-neutronclient >= 2.3.11
Requires:       python-oslo-concurrency >= 1.8.0
Requires:       python-oslo-config >= 2:1.9.3
Requires:       python-oslo-context >= 0.2.0
Requires:       python-oslo-db >= 1.7.0
Requires:       python-oslo-i18n >= 1.5.0
Requires:       python-oslo-log >= 1.0.0
Requires:       python-oslo-messaging >= 1.8.0
Requires:       python-oslo-middleware >= 1.0.0
Requires:       python-oslo-policy >= 0.3.1
Requires:       python-oslo-rootwrap >= 1.6.0
Requires:       python-oslo-serialization >= 1.4.0
Requires:       python-oslo-utils >= 1.4.0
Requires:       python-paste
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-pbr >= 0.6
Requires:       python-pecan >= 0.8.0
Requires:       python-psutil >= 1.1.1
Requires:       python-routes >= 1.12.3
Requires:       python-requests >= 2.2.0
Requires:       python-six >= 1.9.0
Requires:       python-sqlalchemy >= 0.9.7
Requires:       python-stevedore >= 1.3.0
Requires:       python-webob >= 1.2.3
Requires:       python-werkzeug >= 0.7
Requires:       sudo


%description -n python-%{service}
%{common_desc}

This package contains the Designate Python library.


%package -n python-%{service}-tests
Summary:        Designate tests
Group:          Applications/System

Requires:       python-%{service} = %{epoch}:%{version}-%{release}


%description -n python-%{service}-tests
%{common_desc}

This package contains Designate test files.


%package common
Summary:        Designate common files
Group:          Applications/System

Requires:       python-%{service} = %{epoch}:%{version}-%{release}


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

# Let's handle dependencies ourseleves
rm -f requirements.txt


%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py build

# Loop through values in designate-dist.conf and make sure that the values
# are substituted into the designate.conf as comments. Some of these values
# will have been uncommented as a way of upstream setting defaults outside
# of the code.
while read name eq value; do
  test "$name" && test "$value" || continue
  sed -ri "0,/^(#)? *$name *=/{s!^(#)? *$name *=.*!# $name = $value!}" etc/%{service}/%{service}.conf.sample
done < %{SOURCE30}

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Remove unused files
rm -rf %{buildroot}%{python2_sitelib}/bin
rm -rf %{buildroot}%{python2_sitelib}/doc
rm -rf %{buildroot}%{python2_sitelib}/tools

# Move rootwrap files to proper location
install -d -m 755 %{buildroot}%{_datarootdir}/%{service}/rootwrap
mv %{buildroot}/usr/etc/%{service}/rootwrap.d/*.filters %{buildroot}%{_datarootdir}/%{service}/rootwrap

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
for sample in %{service} rootwrap; do
    mv %{buildroot}/usr/etc/%{service}/$sample.conf.sample %{buildroot}%{_sysconfdir}/%{service}/$sample.conf
done
mv %{buildroot}/usr/etc/%{service}/* %{buildroot}%{_sysconfdir}/%{service}
mv %{buildroot}%{_sysconfdir}/%{service}/api-paste.ini %{buildroot}%{_datadir}/%{service}/api-paste.ini

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

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{service}

# Install dist conf
install -p -D -m 640 %{SOURCE30} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf


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


%preun zone-manager
%systemd_preun designate-zone-manager.service


%postun zone-manager
%systemd_postun_with_restart designate-zone-manager.service


%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests


%files -n python-%{service}
%license LICENSE
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-*.egg-info
%exclude %{python2_sitelib}/%{service}/tests


%files common
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/%{service}
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %{_sysconfdir}/%{service}/rootwrap.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%config %{_sysconfdir}/sudoers.d/%{service}
%dir %attr(0755, %{service}, %{service}) %{_sharedstatedir}/%{service}
%dir %attr(0750, %{service}, %{service}) %{_localstatedir}/log/%{service}
%{_bindir}/designate-rootwrap
%dir %{_datarootdir}/%{service}
%dir %{_datarootdir}/%{service}/rootwrap
%{_datarootdir}/%{service}/rootwrap/bind9.filters


%files agent
%license LICENSE
%{_bindir}/designate-agent
%{_unitdir}/designate-agent.service


%files api
%license LICENSE
%{_bindir}/designate-api
%{_unitdir}/designate-api.service
%attr(-, root, %{service}) %{_datadir}/%{service}/api-paste.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/policy.json


%files central
%license LICENSE
%{_bindir}/designate-central
%{_bindir}/designate-manage
%{_unitdir}/designate-central.service


%files mdns
%license LICENSE
%{_bindir}/designate-mdns
%{_unitdir}/designate-mdns.service


%files pool-manager
%license LICENSE
%{_bindir}/designate-pool-manager
%{_unitdir}/designate-pool-manager.service


%files sink
%license LICENSE
%{_bindir}/designate-sink
%{_unitdir}/designate-sink.service


%files zone-manager
%license LICENSE
%{_bindir}/designate-zone-manager
%{_unitdir}/designate-zone-manager.service


%changelog
* Thu Mar 24 2016 RDO <rdo-list@redhat.com> 2.0.0-0.1.0rc1
- RC1 Rebuild for Mitaka rc1
