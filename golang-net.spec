%define prerelease 84a4013f96e01fdd14b65d260a78b543e3702ee1
%define import_path code.google.com/p/go.net
%define gopath %{_prefix}/lib/golang
%define gosrc %{gopath}/src/%{import_path}
%define shortcommit %(c=%{prerelease}; echo ${c:0:12})

Summary:	Supplementary Go networking libraries
Name:		golang-net
Version:	0.1.git%{shortcommit}
Release:	10
License:	BSD
Group:		Development/Other
Url:		http://net.go.googlecode.com
Source0:	http://net.go.googlecode.com/archive/%{prerelease}.zip
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/dict) = %{version}-%{release}
Provides:       golang(%{import_path}/html) = %{version}-%{release}
Provides:       golang(%{import_path}/html/atom) = %{version}-%{release}
Provides:       golang(%{import_path}/idna) = %{version}-%{release}
Provides:       golang(%{import_path}/ipv4) = %{version}-%{release}
Provides:       golang(%{import_path}/ipv6) = %{version}-%{release}
Provides:       golang(%{import_path}/proxy) = %{version}-%{release}
Provides:       golang(%{import_path}/publicsuffix) = %{version}-%{release}
Provides:       golang(%{import_path}/spdy) = %{version}-%{release}
Provides:       golang(%{import_path}/websocket) = %{version}-%{release}

%package devel
BuildRequires:  golang >= 1.3.3
Requires:       golang >= 1.3.3
Summary:        Supplementary Go networking libraries

%description devel
Supplementary Go networking libraries devel part

%description
Supplementary Go networking libraries

%prep
cd %{_builddir}
rm -rf net.go-*
unzip %{SOURCE0}

%build
cd %{_builddir}/net.go-%{shortcommit}
#go build

%install
mkdir -p %{buildroot}%{gosrc}
cp -av %{_builddir}/net.go-%{shortcommit}/* %{buildroot}%{gosrc}/
rm -vf %{buildroot}%{gosrc}/LICENSE
rm -vf %{buildroot}%{gosrc}/README
rm -vf %{buildroot}%{gosrc}/AUTHORS
rm -vf %{buildroot}%{gosrc}/CONTRIBUTORS
rm -vf %{buildroot}%{gosrc}/PATENTS

%files
%doc net.go-%{shortcommit}/README
%doc net.go-%{shortcommit}/LICENSE

%files devel
%doc net.go-%{shortcommit}/LICENSE
%doc net.go-%{shortcommit}/README
%doc net.go-%{shortcommit}/AUTHORS
%doc net.go-%{shortcommit}/CONTRIBUTORS
%doc net.go-%{shortcommit}/PATENTS
%{gosrc}/*


%changelog
* Thu Feb 13 2020 umeabot <umeabot> 0.1.git84a4013f96e0-10.mga8
+ Revision: 1512684
- Mageia 8 Mass Rebuild

* Sun Sep 23 2018 umeabot <umeabot> 0.1.git84a4013f96e0-9.mga7
+ Revision: 1298021
- Mageia 7 Mass Rebuild

* Thu Jun 02 2016 joequant <joequant> 0.1.git84a4013f96e0-8.mga6
+ Revision: 1019893
- fix root dir

* Thu Jun 02 2016 joequant <joequant> 0.1.git84a4013f96e0-7.mga6
+ Revision: 1019877
- fix golang path

* Tue Feb 09 2016 umeabot <umeabot> 0.1.git84a4013f96e0-6.mga6
+ Revision: 952193
- Mageia 6 Mass Rebuild

* Thu Jan 22 2015 bcornec <bcornec> 0.1.git84a4013f96e0-5.mga5
+ Revision: 811829
- Split the package in 2 with a devel one containing the .go files

* Wed Oct 15 2014 umeabot <umeabot> 0.1.git84a4013f96e0-4.mga5
+ Revision: 747403
- Second Mageia 5 Mass Rebuild

* Tue Sep 16 2014 umeabot <umeabot> 0.1.git84a4013f96e0-3.mga5
+ Revision: 679875
- Mageia 5 Mass Rebuild

* Mon Jun 30 2014 bcornec <bcornec> 0.1.git84a4013f96e0-2.mga5
+ Revision: 641555
- Fix for golang FHS

* Sat Dec 21 2013 thatsamguy <thatsamguy> 0.1.git84a4013f96e0-1.mga4
+ Revision: 559388
- imported package golang-net

