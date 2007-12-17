#Module-Specific definitions
%define mod_name mod_tidy
%define mod_conf 31_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Mod_tidy is a DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	0.5.5
Release:	%mkrel 4
Group:		System/Servers
License:	Apache License
URL:		http://mod-tidy.sourceforge.net/
Source0:	http://www.gknw.at/development/apache/httpd-2.0/unix/modules/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}.bz2
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.0.55
Requires(pre):	apache >= 2.0.55
Requires:	apache-conf >= 2.0.55
Requires:	apache >= 2.0.55
BuildRequires:	apache-devel >= 2.0.55
BuildRequires:	tidy-devel
BuildRequires:	file
Epoch:		1

%description
mod_tidy is a TidyLib based DSO module for the Apache HTTP Server
Version 2 to parse, clean-up and pretty-print the webservers'
(X)HTML output.

%prep

%setup -q -n %{mod_name}-%{version}

# fix strange perms
chmod 644 README Changes

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
 
%{_sbindir}/apxs -ltidy -c src/%{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

cp -rp src/.libs .

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README Changes
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


