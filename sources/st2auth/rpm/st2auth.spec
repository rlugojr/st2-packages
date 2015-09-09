%define package st2auth
%define _sourcedir /root/code
%define specdir /root/code/rpmspec
%include %{specdir}/package_top.spec

Summary: St2Auth - StackStorm authentication service component
Requires: st2common = %{version}-%{release}

%include %{specdir}/package_venv.spec
%include %{specdir}/helpers.spec

%description
  <insert long description, indented with spaces>

%install
  %default_install
  %pip_install_venv

  # systemd service file
  mkdir -p %{buildroot}%{_unitdir}
  install -m0644 %{SOURCE0}/rpm/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
  make post_install DESTDIR=%{?buildroot}

%prep
  rm -rf %{buildroot}
  mkdir -p %{buildroot}

%clean
  rm -rf %{buildroot}

%post
  %systemd_post %{name}
  systemctl --no-reload enable %{name} >/dev/null 2>&1 || :

%preun
  %systemd_preun %{name}

%postun
  %systemd_postun

%files
  %{_datadir}/python/%{name}
  %config(noreplace) %{_sysconfdir}/st2/*
  %{_unitdir}/%{name}.service