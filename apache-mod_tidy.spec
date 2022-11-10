#Module-Specific definitions
%define mod_name mod_tidy
%define mod_conf 31_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	DSO module for the apache web server
Name:		apache-%{mod_name}
Version:	0.5.5
Release:	15
Group:		System/Servers
License:	Apache License
URL:		https://mod-tidy.sourceforge.net/
Source0:	https://mod-tidy.sourceforge.net/src/%{mod_name}-%{version}.tar.gz
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

%autosetup  -n %{mod_name}-%{version}

# fix strange perms
chmod 644 README Changes

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
 
%{_bindir}/apxs -ltidy -c src/%{mod_name}.c

%install

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

%files
%doc README Changes
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*




%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.5-13mdv2012.0
+ Revision: 772773
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.5-12
+ Revision: 678427
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.5-11mdv2011.0
+ Revision: 588073
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.5-10mdv2010.1
+ Revision: 516189
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.5-9mdv2010.0
+ Revision: 406661
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.5-8mdv2009.0
+ Revision: 235112
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.5-7mdv2009.0
+ Revision: 215653
- fix rebuild

* Sun Mar 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.5-6mdv2008.1
+ Revision: 182871
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1:0.5.5-5mdv2008.1
+ Revision: 170754
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Dec 14 2007 Thierry Vignaud <tv@mandriva.org> 1:0.5.5-4mdv2008.1
+ Revision: 119826
- rebuild b/c of missing package on ia32

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.5-3mdv2008.0
+ Revision: 82685
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.5.5-2mdv2007.1
+ Revision: 140763
- rebuild

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.5-1mdv2007.0
+ Revision: 79525
- Import apache-mod_tidy

* Mon Jul 03 2006 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.5-1mdv2007.0
- 0.5.5
- drop upstream apache220 patch (P0)

* Fri Dec 16 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.3-2mdk
- rebuilt against apache-2.2.0 (P0)

* Mon Nov 28 2005 Oden Eriksson <oeriksson@mandriva.com> 1:0.5.3-1mdk
- 0.5.3
- fix versioning

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.5-1mdk
- 0.5
- new upstream maintainer (Sierk Bornemann)

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.3-2mdk
- fix deps

* Fri Jun 03 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_0.3-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.3-4mdk
- use the %1

* Mon Feb 28 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.3-3mdk
- fix %%post and %%postun to prevent double restarts
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.3-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_0.3-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_0.3-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_0.3-1mdk
- built for apache 2.0.51

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_0.3-1mdk
- built for apache 2.0.50
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_0.3-1mdk
- built for apache 2.0.49

