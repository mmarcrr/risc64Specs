%{?scl:%scl_package docker-client}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}docker-client
Version:        4.0.6
Release:        3%{?dist}
Summary:        Docker Client

License:        ASL 2.0
URL:            https://github.com/spotify/docker-client
Source0:        https://github.com/spotify/docker-client/archive/v%{version}.tar.gz

Patch0:         add-manifest.patch
Patch1:         httpcomponents-annotations.patch

BuildRequires: maven-local
BuildRequires: mvn(org.apache.maven.plugins:maven-failsafe-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires: mvn(org.jacoco:jacoco-maven-plugin)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires: %{?scl_prefix}apache-commons-compress >= 1.9
BuildRequires: %{?scl_prefix}bouncycastle-pkix >= 1.50
BuildRequires: %{?scl_prefix}glassfish-hk2-utils >= 2.4.0-0.4.b24
BuildRequires: %{?scl_prefix}jnr-unixsocket >= 0.2
BuildRequires: %{?scl_prefix}glassfish-annotation-api >= 1.2
BuildRequires: %{?scl_prefix}glassfish-hk2-api >= 2.4.0-0.4.b24
BuildRequires: %{?scl_prefix}glassfish-hk2-locator >= 2.4.0-0.4.b24
BuildRequires: %{?scl_prefix}glassfish-jaxb-api >= 2.2.12
BuildRequires: %{?scl_prefix}glassfish-jax-rs-api >= 2.0.1
BuildRequires: %{?scl_prefix}jackson-annotations >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-core >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-databind >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-dataformat-yaml >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-datatype-guava >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-jaxrs-json-provider >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-jaxrs-providers >= 2.5.0
BuildRequires: %{?scl_prefix}jackson-module-jaxb-annotations >= 2.5.0
BuildRequires: %{?scl_prefix}jersey >= 2.17

# This is provided by JRE but need it until either
# - jackson-module-jaxb-annotations adds Requires to it
# - jackson-module-jaxb-annotations removes it from Import-Package entirely
Requires: %{?scl_prefix}glassfish-jaxb-api >= 2.2.12

# API change in httpcomponents makes this version important
%if 0%{fedora} >= 25
Requires: httpcomponents-core >= 4.4.5
%endif

BuildArch: noarch

%description
The Docker Client is a Java API library for accessing a Docker daemon.

%prep
%setup -q -n docker-client-%{version}
%patch0
%if 0%{fedora} >= 25
%patch1
%endif
%pom_remove_plugin org.sonatype.plugins:nexus-staging-maven-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-checkstyle-plugin
%pom_remove_plugin org.apache.maven.plugins:maven-shade-plugin

%build
%mvn_build -j -f

%install
%mvn_install

%files -f .mfiles
%license LICENSE
%doc NOTICE README.md

%changelog
* Thu Jun 30 2016 Mat Booth <mat.booth@redhat.com> - 4.0.6-3
- Add missing BR on oss-parent
- Add patch to avoid annotations removed from httpcomponents

* Wed Jun 29 2016 Mat Booth <mat.booth@redhat.com> - 4.0.6-2
- Add missing import-packages in OSGi manifest

* Thu May 19 2016 Alexander Kurtakov <akurtako@redhat.com> 4.0.6-1
- Update to upstream 4.0.6 release.

* Tue Apr 19 2016 Roland Grunberg <rgrunber@redhat.com> - 4.0.1-2
- Add com.spotify.docker.client.exceptions to exported packages.

* Mon Apr 18 2016 Alexander Kurtakov <akurtako@redhat.com> 4.0.1-1
- Update to upstream 4.0.1 release.

* Wed Apr 6 2016 Alexander Kurtakov <akurtako@redhat.com> 3.6.8-1
- Update to upstream 3.6.8 release.

* Fri Mar 25 2016 Alexander Kurtakov <akurtako@redhat.com> 3.6.6-1
- Update to upstream 3.6.6 release.

* Thu Feb 11 2016 Alexander Kurtakov <akurtako@redhat.com> 3.5.12-1
- Update to upstream 3.5.12 release.

* Mon Feb 8 2016 Alexander Kurtakov <akurtako@redhat.com> 3.5.11-1
- Update to upstream 3.5.11 release.

* Thu Feb 4 2016 Alexander Kurtakov <akurtako@redhat.com> 3.5.10-1
- Update to upstream 3.5.10 release.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Alexander Kurtakov <akurtako@redhat.com> 3.5.9-1
- Update to upstream 3.5.9 release.

* Fri Oct 23 2015 Alexander Kurtakov <akurtako@redhat.com> 3.1.9-1
- Update to upstream 3.1.9 release.

* Tue Oct 6 2015 akurtakov <akurtakov@localhost.localdomain> 3.1.5-1
- Update to upstream 3.1.5.
- Stripdown useless BRs.

* Thu Sep 24 2015 Alexander Kurtakov <akurtako@redhat.com> 3.1.4-1
- Update to upstream 3.1.4 release.

* Mon Aug 17 2015 Alexander Kurtakov <akurtako@redhat.com> 3.1.3-1
- Update to upstream 3.1.3 release.

* Wed Aug 5 2015 Alexander Kurtakov <akurtako@redhat.com> 3.1.2-1
- Update to upstream 3.1.2 release.

* Thu Jul 30 2015 Roland Grunberg <rgrunber@redhat.com> - 3.1.1-2
- Update manifest's Bundle-Version to match %%{version}.

* Thu Jul 30 2015 Alexander Kurtakov <akurtako@redhat.com> 3.1.1-1
- Update to upstream 3.1.1 release.

* Wed Jul 22 2015 Roland Grunberg <rgrunber@redhat.com> - 3.0.0-2
- Support the 1.19 Docker Remote API.
- Support SO_LINGER option needed when httpcomponents-core >= 4.4.

* Wed Jul 08 2015 Roland Grunberg <rgrunber@redhat.com> - 3.0.0-1
- Update to 3.0.0.

* Wed Jun 24 2015 Roland Grunberg <rgrunber@redhat.com> - 2.7.26-3
- Depend upon hk2-locator as it's needed by jersey-client at runtime.
- Require jaxb-api to temporarily satisfy an invalid requirement.

* Tue Jun 23 2015 Roland Grunberg <rgrunber@redhat.com> - 2.7.26-2
- Depend on versionless bouncycastle within manifest.

* Mon Jun 8 2015 Jeff Johnston <jjohnstn@redhat.com> 2.7.26-1
- Initial packaging.
