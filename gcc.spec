%global DATE 20200826
%global gitrev c59c8927f43fb78d6a72a0ff93a47b36e43282d5
%global gcc_version 10.2.1
%global gcc_major 10
# Note, gcc_release must be integer, if you want to add suffixes to
# %%{release}, append them after %%{gcc_release} on Release: line.
%global gcc_release 3
%global nvptx_tools_gitrev 5f6f343a302d620b0868edab376c00b15741e39e
%global newlib_cygwin_gitrev 50e2a63b04bdd018484605fbb954fd1bd5147fa0
%global _unpackaged_files_terminate_build 0
%global _performance_build 1
# Hardening slows the compiler way too much.
%undefine _hardened_build
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
# Until annobin is fixed (#1519165).
%undefine _annotated_build
%endif
# Strip will fail on nvptx-none *.a archives and the brp-* scripts will
# fail randomly depending on what is stripped last.
%if 0%{?__brp_strip_static_archive:1}
%global __brp_strip_static_archive %{__brp_strip_static_archive} || :
%endif
%if 0%{?__brp_strip_lto:1}
%global __brp_strip_lto %{__brp_strip_lto} || :
%endif
%if 0%{?fedora} < 32 && 0%{?rhel} < 8
%global multilib_64_archs sparc64 ppc64 ppc64p7 s390x x86_64
%else
%global multilib_64_archs sparc64 ppc64 ppc64p7 x86_64
%endif
%if 0%{?rhel} > 7
%global build_ada 0
%global build_objc 0
%global build_go 0
%global build_d 0
%else
%ifarch %{ix86} x86_64 ia64 ppc %{power64} alpha s390x %{arm} aarch64 riscv64
%global build_ada 1
%else
%global build_ada 0
%endif
%global build_objc 1
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips} riscv64
%global build_go 1
%else
%global build_go 0
%endif
%ifarch %{ix86} x86_64 %{arm} %{mips} s390 s390x riscv64
%global build_d 1
%else
%global build_d 0
%endif
%endif
%ifarch %{ix86} x86_64 ia64 ppc64le
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64
%global build_libasan 1
%else
%global build_libasan 0
%endif
%ifarch x86_64 ppc64 ppc64le aarch64
%global build_libtsan 1
%else
%global build_libtsan 0
%endif
%ifarch x86_64 ppc64 ppc64le aarch64
%global build_liblsan 1
%else
%global build_liblsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64
%global build_libubsan 1
%else
%global build_libubsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips} riscv64
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64 ppc64le ppc64p7 s390 s390x aarch64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%if 0%{?rhel} > 8
%global build_isl 0
%else
%global build_isl 1
%endif
%global build_libstdcxx_docs 1
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global attr_ifunc 1
%else
%global attr_ifunc 0
%endif
%ifarch x86_64 ppc64le
%global build_offload_nvptx 1
%else
%global build_offload_nvptx 0
%endif
%if 0%{?fedora} < 32 && 0%{?rhel} < 8
%ifarch s390x
%global multilib_32_arch s390
%endif
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64 ppc64p7
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%global multilib_32_arch i686
%endif
Summary: Various compilers (C, C++, Objective-C, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
# libgcc, libgfortran, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone --depth 1 git://gcc.gnu.org/git/gcc.git gcc-dir.tmp
# git --git-dir=gcc-dir.tmp/.git fetch --depth 1 origin %%{gitrev}
# git --git-dir=gcc-dir.tmp/.git archive --prefix=%%{name}-%%{version}-%%{DATE}/ %%{gitrev} | xz -9e > %%{name}-%%{version}-%%{DATE}.tar.xz
# rm -rf gcc-dir.tmp
Source0: gcc-%{version}-%{DATE}.tar.xz
# The source for nvptx-tools package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone --depth 1 git://github.com/MentorEmbedded/nvptx-tools.git nvptx-tools-dir.tmp
# git --git-dir=nvptx-tools-dir.tmp/.git fetch --depth 1 origin %%{nvptx_tools_gitrev}
# git --git-dir=nvptx-tools-dir.tmp/.git archive --prefix=nvptx-tools-%%{nvptx_tools_gitrev}/ %%{nvptx_tools_gitrev} | xz -9e > nvptx-tools-%%{nvptx_tools_gitrev}.tar.xz
# rm -rf nvptx-tools-dir.tmp
Source1: nvptx-tools-%{nvptx_tools_gitrev}.tar.xz
# The source for nvptx-newlib package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone git://sourceware.org/git/newlib-cygwin.git newlib-cygwin-dir.tmp
# git --git-dir=newlib-cygwin-dir.tmp/.git archive --prefix=newlib-cygwin-%%{newlib_cygwin_gitrev}/ %%{newlib_cygwin_gitrev} ":(exclude)newlib/libc/sys/linux/include/rpc/*.[hx]" | xz -9e > newlib-cygwin-%%{newlib_cygwin_gitrev}.tar.xz
# rm -rf newlib-cygwin-dir.tmp
Source2: newlib-cygwin-%{newlib_cygwin_gitrev}.tar.xz
%global isl_version 0.16.1
URL: http://gcc.gnu.org
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %%gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
# Need binutils which support -plugin
# Need binutils which support .loc view >= 2.30
# Need binutils which support --generate-missing-build-notes=yes >= 2.31
%if 0%{?fedora} >= 29 || 0%{?rhel} > 7
BuildRequires: binutils >= 2.31
%else
BuildRequires: binutils >= 2.24
%endif
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, sharutils
BuildRequires: texinfo, texinfo-tex, /usr/bin/pod2man
BuildRequires: systemtap-sdt-devel >= 1.3
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 3.1.0, libmpc-devel >= 0.8.1
BuildRequires: python3-devel, /usr/bin/python
BuildRequires: gcc, gcc-c++
%if %{build_go}
BuildRequires: hostname, procps
%endif
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
BuildRequires: libzstd-devel
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
%if %{build_isl}
BuildRequires: isl = %{isl_version}
BuildRequires: isl-devel = %{isl_version}
%if 0%{?__isa_bits} == 64
Requires: libisl.so.15()(64bit)
%else
Requires: libisl.so.15
%endif
%endif
%if %{build_libstdcxx_docs}
BuildRequires: doxygen >= 1.7.1
BuildRequires: graphviz, dblatex, texlive-collection-latex, docbook5-style-xsl
%endif
Requires: cpp = %{version}-%{release}
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils that support --build-id
# Need binutils that support %%gnu_unique_object
# Need binutils that support .cfi_sections
# Need binutils that support --no-add-needed
# Need binutils that support -plugin
# Need binutils that support .loc view >= 2.30
# Need binutils which support --generate-missing-build-notes=yes >= 2.31
%if 0%{?fedora} >= 29 || 0%{?rhel} > 7
Requires: binutils >= 2.31
%else
Requires: binutils >= 2.24
%endif
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%ifarch %{arm}
Requires: glibc >= 2.16
%endif
%endif
Requires: libgcc >= %{version}-%{release}
Requires: libgomp = %{version}-%{release}
%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
%endif
Obsoletes: gcc-java < %{version}-%{release}
AutoReq: true
Provides: bundled(libiberty)
Provides: gcc(major) = %{gcc_major}

Patch0: gcc10-hack.patch
Patch1: gcc10-i386-libgomp.patch
Patch2: gcc10-sparc-config-detection.patch
Patch3: gcc10-libgomp-omp_h-multilib.patch
Patch4: gcc10-libtool-no-rpath.patch
Patch5: gcc10-isl-dl.patch
Patch6: gcc10-libstdc++-docs.patch
Patch7: gcc10-no-add-needed.patch
Patch8: gcc10-foffload-default.patch
Patch9: gcc10-Wno-format-security.patch
Patch10: gcc10-rh1574936.patch
Patch11: gcc10-d-shared-libphobos.patch
Patch12: gcc10-pr96383.patch
Patch13: gcc10-pr96385.patch
Patch14: gcc10-pr96690.patch

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%global _gnu %{nil}
%else
%global _gnu -gnueabi
%endif
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc ppc64p7
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparcv9 ppc ppc64p7
%global gcc_target_platform %{_target_platform}
%endif

%if %{build_go}
# Avoid stripping these libraries and binaries.
%global __os_install_post \
chmod 644 %{buildroot}%{_prefix}/%{_lib}/libgo.so.16.* \
chmod 644 %{buildroot}%{_prefix}/bin/go.gcc \
chmod 644 %{buildroot}%{_prefix}/bin/gofmt.gcc \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet \
%__os_install_post \
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgo.so.16.* \
chmod 755 %{buildroot}%{_prefix}/bin/go.gcc \
chmod 755 %{buildroot}%{_prefix}/bin/gofmt.gcc \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet \
%{nil}
%endif

%description
The gcc package contains the GNU Compiler Collection version 10.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version 10 shared support library
Autoreq: false
%if !%{build_ada}
Obsoletes: libgnat < %{version}-%{release}
%endif
Obsoletes: libmudflap
Obsoletes: libmudflap-devel
Obsoletes: libmudflap-static
Obsoletes: libgcj < %{version}-%{release}
Obsoletes: libgcj-devel < %{version}-%{release}
Obsoletes: libgcj-src < %{version}-%{release}
%ifarch %{ix86} x86_64
Obsoletes: libcilkrts
Obsoletes: libcilkrts-static
Obsoletes: libmpx
Obsoletes: libmpx-static
%endif

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Requires: gcc = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Provides: gcc-g++ = %{version}-%{release}
Provides: g++ = %{version}-%{release}
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Autoreq: true
Requires: glibc >= 2.10.90-7

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Requires: libstdc++%{?_isa} = %{version}-%{release}
Autoreq: true

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n libstdc++-static
Summary: Static libraries for the GNU standard C++ library
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description -n libstdc++-static
Static libraries for the GNU standard C++ library.

%package -n libstdc++-docs
Summary: Documentation for the GNU standard C++ library
Autoreq: true

%description -n libstdc++-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%package objc
Summary: Objective-C support for GCC
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
Autoreq: true

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Requires: gcc-c++ = %{version}-%{release}, gcc-objc = %{version}-%{release}
Autoreq: true

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Autoreq: true

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%package gfortran
Summary: Fortran support
Requires: gcc = %{version}-%{release}
Requires: libgfortran = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath = %{version}-%{release}
Requires: libquadmath-devel = %{version}-%{release}
%endif
Provides: gcc-fortran = %{version}-%{release}
Provides: gfortran = %{version}-%{release}
Autoreq: true

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
Autoreq: true
%if %{build_libquadmath}
Requires: libquadmath = %{version}-%{release}
%endif

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgfortran-static
Summary: Static Fortran libraries
Requires: libgfortran = %{version}-%{release}
Requires: gcc = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath-static = %{version}-%{release}
%endif

%description -n libgfortran-static
This package contains static Fortran libraries.

%package gdc
Summary: D support
Requires: gcc = %{version}-%{release}
Requires: libgphobos = %{version}-%{release}
Provides: gcc-d = %{version}-%{release}
Provides: gdc = %{version}-%{release}
Autoreq: true

%description gdc
The gcc-gdc package provides support for compiling D
programs with the GNU Compiler Collection.

%package -n libgphobos
Summary: D runtime
Autoreq: true

%description -n libgphobos
This package contains D shared library which is needed to run
D dynamically linked programs.

%package -n libgphobos-static
Summary: Static D libraries
Requires: libgphobos = %{version}-%{release}
Requires: gcc-gdc = %{version}-%{release}

%description -n libgphobos-static
This package contains static D libraries.

%package -n libgomp
Summary: GCC OpenMP v4.5 shared support library

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v4.5 support.

%package -n libgomp-offload-nvptx
Summary: GCC OpenMP v4.5 plugin for offloading to NVPTX
Requires: libgomp = %{version}-%{release}

%description -n libgomp-offload-nvptx
This package contains libgomp plugin for offloading to NVidia
PTX.  The plugin needs libcuda.so.1 shared library that has to be
installed separately.

%package gdb-plugin
Summary: GCC plugin for GDB
Requires: gcc = %{version}-%{release}

%description gdb-plugin
This package contains GCC plugin for GDB C expression evaluation.

%package -n libgccjit
Summary: Library for embedding GCC inside programs and libraries
Requires: gcc = %{version}-%{release}

%description -n libgccjit
This package contains shared library with GCC JIT front-end.

%package -n libgccjit-devel
Summary: Support for embedding GCC inside programs and libraries
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
BuildRequires: python3-sphinx
%else
BuildRequires: python-sphinx
%endif
Requires: libgccjit = %{version}-%{release}

%description -n libgccjit-devel
This package contains header files and documentation for GCC JIT front-end.

%package -n libquadmath
Summary: GCC __float128 shared support library

%description -n libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n libquadmath-devel
Summary: GCC __float128 support
Requires: libquadmath = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libquadmath-devel
This package contains headers for building Fortran programs using
REAL*16 and programs using __float128 math.

%package -n libquadmath-static
Summary: Static libraries for __float128 support
Requires: libquadmath-devel = %{version}-%{release}

%description -n libquadmath-static
This package contains static libraries for building Fortran programs
using REAL*16 and programs using __float128 math.

%package -n libitm
Summary: The GNU Transactional Memory library

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libitm-devel
Summary: The GNU Transactional Memory support
Requires: libitm = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libitm-devel
This package contains headers and support files for the
GNU Transactional Memory library.

%package -n libitm-static
Summary: The GNU Transactional Memory static library
Requires: libitm-devel = %{version}-%{release}

%description -n libitm-static
This package contains GNU Transactional Memory static libraries.

%package -n libatomic
Summary: The GNU Atomic library

%description -n libatomic
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n libatomic-static
Summary: The GNU Atomic static library
Requires: libatomic = %{version}-%{release}

%description -n libatomic-static
This package contains GNU Atomic static libraries.

%package -n libasan
Summary: The Address Sanitizer runtime library

%description -n libasan
This package contains the Address Sanitizer library
which is used for -fsanitize=address instrumented programs.

%package -n libasan-static
Summary: The Address Sanitizer static library
Requires: libasan = %{version}-%{release}

%description -n libasan-static
This package contains Address Sanitizer static runtime library.

%package -n libtsan
Summary: The Thread Sanitizer runtime library

%description -n libtsan
This package contains the Thread Sanitizer library
which is used for -fsanitize=thread instrumented programs.

%package -n libtsan-static
Summary: The Thread Sanitizer static library
Requires: libtsan = %{version}-%{release}

%description -n libtsan-static
This package contains Thread Sanitizer static runtime library.

%package -n libubsan
Summary: The Undefined Behavior Sanitizer runtime library

%description -n libubsan
This package contains the Undefined Behavior Sanitizer library
which is used for -fsanitize=undefined instrumented programs.

%package -n libubsan-static
Summary: The Undefined Behavior Sanitizer static library
Requires: libubsan = %{version}-%{release}

%description -n libubsan-static
This package contains Undefined Behavior Sanitizer static runtime library.

%package -n liblsan
Summary: The Leak Sanitizer runtime library

%description -n liblsan
This package contains the Leak Sanitizer library
which is used for -fsanitize=leak instrumented programs.

%package -n liblsan-static
Summary: The Leak Sanitizer static library
Requires: liblsan = %{version}-%{release}

%description -n liblsan-static
This package contains Leak Sanitizer static runtime library.

%package -n cpp
Summary: The C Preprocessor
Requires: filesystem >= 3
Provides: /lib/cpp
Autoreq: true

%description -n cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%package gnat
Summary: Ada 83, 95, 2005 and 2012 support for GCC
Requires: gcc = %{version}-%{release}
Requires: libgnat = %{version}-%{release}, libgnat-devel = %{version}-%{release}
Autoreq: true

%description gnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
development tools, the documents and Ada compiler.

%package -n libgnat
Summary: GNU Ada 83, 95, 2005 and 2012 runtime shared libraries
Autoreq: true

%description -n libgnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
shared libraries, which are required to run programs compiled with the GNAT.

%package -n libgnat-devel
Summary: GNU Ada 83, 95, 2005 and 2012 libraries
Autoreq: true

%description -n libgnat-devel
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
libraries, which are required to compile with the GNAT.

%package -n libgnat-static
Summary: GNU Ada 83, 95, 2005 and 2012 static libraries
Requires: libgnat-devel = %{version}-%{release}
Autoreq: true

%description -n libgnat-static
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
static libraries.

%package go
Summary: Go support
Requires: gcc = %{version}-%{release}
Requires: libgo = %{version}-%{release}
Requires: libgo-devel = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Provides: gccgo = %{version}-%{release}
Autoreq: true

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%package -n libgo
Summary: Go runtime
Autoreq: true

%description -n libgo
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%package -n libgo-devel
Summary: Go development libraries
Requires: libgo = %{version}-%{release}
Autoreq: true

%description -n libgo-devel
This package includes libraries and support files for compiling
Go programs.

%package -n libgo-static
Summary: Static Go libraries
Requires: libgo = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libgo-static
This package contains static Go libraries.

%package plugin-devel
Summary: Support for compiling GCC plugins
Requires: gcc = %{version}-%{release}
Requires: gmp-devel >= 4.1.2-8, mpfr-devel >= 3.1.0, libmpc-devel >= 0.8.1

%description plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%package offload-nvptx
Summary: Offloading compiler to NVPTX
Requires: gcc = %{version}-%{release}
Requires: libgomp-offload-nvptx = %{version}-%{release}

%description offload-nvptx
The gcc-offload-nvptx package provides offloading support for
NVidia PTX.  OpenMP and OpenACC programs linked with -fopenmp will
by default add PTX code into the binaries, which can be offloaded
to NVidia PTX capable devices if available.

%prep
%setup -q -n gcc-%{version}-%{DATE} -a 1 -a 2
%patch0 -p0 -b .hack~
%patch1 -p0 -b .i386-libgomp~
%patch2 -p0 -b .sparc-config-detection~
%patch3 -p0 -b .libgomp-omp_h-multilib~
%patch4 -p0 -b .libtool-no-rpath~
%if %{build_isl}
%patch5 -p0 -b .isl-dl~
%endif
%if %{build_libstdcxx_docs}
%patch6 -p0 -b .libstdc++-docs~
%endif
%patch7 -p0 -b .no-add-needed~
%patch8 -p0 -b .foffload-default~
%patch9 -p0 -b .Wno-format-security~
%if 0%{?fedora} >= 29 || 0%{?rhel} > 7
%patch10 -p0 -b .rh1574936~
%endif
%patch11 -p0 -b .d-shared-libphobos~
%patch12 -p0 -b .pr96383~
%patch13 -p0 -b .pr96385~
%patch14 -p0 -b .pr96690~

echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

# This test causes fork failures, because it spawns way too many threads
rm -f gcc/testsuite/go.test/test/chan/goroutines.go

%build

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

CC=gcc
CXX=g++
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-flto=auto//g;s/-flto//g;s/-ffat-lto-objects//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Werror=format-security/-Wformat-security/g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables /' \
      libgcc/Makefile.in
    ;;
esac

%if %{build_offload_nvptx}
mkdir obji
IROOT=`pwd`/obji
cd nvptx-tools-%{nvptx_tools_gitrev}
rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}
CC="$CC" CXX="$CXX" CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" \
../configure --prefix=%{_prefix}
make %{?_smp_mflags}
make install prefix=${IROOT}%{_prefix}
cd ../..

ln -sf newlib-cygwin-%{newlib_cygwin_gitrev}/newlib newlib
rm -rf obj-offload-nvptx-none
mkdir obj-offload-nvptx-none

cd obj-offload-nvptx-none
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --disable-bootstrap --disable-sjlj-exceptions \
	--enable-newlib-io-long-long --with-build-time-tools=${IROOT}%{_prefix}/nvptx-none/bin \
	--target nvptx-none --enable-as-accelerator-for=%{gcc_target_platform} \
	--enable-languages=c,c++,fortran,lto \
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla \
	--enable-checking=release --with-system-zlib \
	--with-gcc-major-version-only --without-isl
make %{?_smp_mflags}
cd ..
rm -f newlib
%endif

rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

enablelgo=
enablelada=
enablelobjc=
enableld=
%if %{build_objc}
enablelobjc=,objc,obj-c++
%endif
%if %{build_ada}
enablelada=,ada
%endif
%if %{build_go}
enablelgo=,go
%endif
%if %{build_d}
enableld=,d
%endif
CONFIGURE_OPTS="\
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla \
	--enable-shared --enable-threads=posix --enable-checking=release \
%ifarch ppc64le
	--enable-targets=powerpcle-linux \
%endif
%ifarch ppc64le %{mips} s390x
%ifarch s390x
%if 0%{?fedora} < 32 && 0%{?rhel} < 8
	--enable-multilib \
%else
	--disable-multilib \
%endif
%else
	--disable-multilib \
%endif
%else
	--enable-multilib \
%endif
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object --enable-linker-build-id --with-gcc-major-version-only \
%ifnarch %{mips}
	--with-linker-hash-style=gnu \
%endif
	--enable-plugin --enable-initfini-array \
%if %{build_isl}
	--with-isl \
%else
	--without-isl \
%endif
%if %{build_offload_nvptx}
	--enable-offload-targets=nvptx-none \
	--without-cuda-driver \
%endif
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
%if %{attr_ifunc}
	--enable-gnu-indirect-function \
%endif
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 ppc64le ppc64p7 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%ifarch ppc ppc64 ppc64p7
%if 0%{?rhel} >= 7
	--with-cpu-32=power7 --with-tune-32=power7 --with-cpu-64=power7 --with-tune-64=power7 \
%endif
%if 0%{?rhel} == 6
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc64le
	--with-cpu-32=power8 --with-tune-32=power8 --with-cpu-64=power8 --with-tune-64=power8 \
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--enable-cet \
	--with-tune=generic \
%endif
%if 0%{?rhel} >= 7
%ifarch %{ix86}
	--with-arch=x86-64 \
%endif
%ifarch x86_64
	--with-arch_32=x86-64 \
%endif
%else
%ifarch %{ix86}
	--with-arch=i686 \
%endif
%ifarch x86_64
	--with-arch_32=i686 \
%endif
%endif
%ifarch s390 s390x
%if 0%{?rhel} >= 7
%if 0%{?rhel} > 7
	--with-arch=zEC12 --with-tune=z13 \
%else
	--with-arch=z196 --with-tune=zEC12 \
%endif
%else
%if 0%{?fedora} >= 26
	--with-arch=zEC12 --with-tune=z13 \
%else
	--with-arch=z9-109 --with-tune=z10 \
%endif
%endif
	--enable-decimal-float \
%endif
%ifarch armv7hl
	--with-tune=generic-armv7-a --with-arch=armv7-a \
	--with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux \
%endif
%ifarch mips mipsel
	--with-arch=mips32r2 --with-fp-32=xx \
%endif
%ifarch mips64 mips64el
	--with-arch=mips64r2 --with-abi=64 \
%endif
%ifarch riscv64
	--with-arch=rv64gc --with-abi=lp64d --with-multilib-list=lp64d \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform} \
%endif
	"

CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --enable-bootstrap \
	--enable-languages=c,c++,fortran${enablelobjc}${enablelada}${enablelgo}${enableld},lto \
	$CONFIGURE_OPTS

%ifarch sparc sparcv9 sparc64
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
%else
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
%endif

CC="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc`"
CXX="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes`"

# Build libgccjit separately, so that normal compiler binaries aren't -fpic
# unnecessarily.
mkdir objlibgccjit
cd objlibgccjit
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../../configure --disable-bootstrap --enable-host-shared \
	--enable-languages=jit $CONFIGURE_OPTS
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" all-gcc
cp -a gcc/libgccjit.so* ../gcc/
cd ../gcc/
ln -sf xgcc %{gcc_target_platform}-gcc-%{gcc_major}
cp -a Makefile{,.orig}
sed -i -e '/^CHECK_TARGETS/s/$/ check-jit/' Makefile
touch -r Makefile.orig Makefile
rm Makefile.orig
make jit.sphinx.html
make jit.sphinx.install-html jit_htmldir=`pwd`/../../rpm.doc/libgccjit-devel/html
cd ..

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/objc rpm.doc/gdc rpm.doc/libphobos
mkdir -p rpm.doc/go rpm.doc/libgo rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer}

for i in {gcc,gcc/cp,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
%if %{build_objc}
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
%endif
%if %{build_d}
(cd gcc/d; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gdc/$i.gdc
done)
(cd libphobos; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libphobos/$i.libphobos
done
cp -a src/LICENSE*.txt libdruntime/LICENSE ../rpm.doc/libphobos/)
%endif
%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
	cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done)
%endif
%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif
%if %{build_go}
(cd gcc/go; for i in README* ChangeLog*; do
	cp -p $i ../../rpm.doc/go/$i
done)
(cd libgo; for i in LICENSE* PATENTS* README; do
	cp -p $i ../rpm.doc/libgo/$i.libgo
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# RISC-V ABI wants to install everything in /lib64/lp64d or /usr/lib64/lp64d.
# Make these be symlinks to /lib64 or /usr/lib64 respectively. See:
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/DRHT5YTPK4WWVGL3GIN5BF2IKX2ODHZ3/
%ifarch riscv64
for d in %{buildroot}%{_libdir} %{buildroot}/%{_lib} \
	  %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib} \
	  %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/%{_lib}; do
  mkdir -p $d
  (cd $d && ln -sf . lp64d)
done
%endif

%if %{build_offload_nvptx}
cd nvptx-tools-%{nvptx_tools_gitrev}
cd obj-%{gcc_target_platform}
make install prefix=%{buildroot}%{_prefix}
cd ../..

ln -sf newlib-cygwin-%{newlib_cygwin_gitrev}/newlib newlib
cd obj-offload-nvptx-none
make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
rm -rf %{buildroot}%{_prefix}/libexec/gcc/nvptx-none/%{gcc_major}/install-tools
rm -rf %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/{install-tools,plugin,cc1,cc1plus,f951}
rm -rf %{buildroot}%{_infodir} %{buildroot}%{_mandir}/man7 %{buildroot}%{_prefix}/share/locale
rm -rf %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/{install-tools,plugin}
rm -rf %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/{install-tools,plugin,include-fixed}
rm -rf %{buildroot}%{_prefix}/%{_lib}/libc[cp]1*
mv -f %{buildroot}%{_prefix}/nvptx-none/lib/*.{a,spec} %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/
mv -f %{buildroot}%{_prefix}/nvptx-none/lib/mgomp/*.{a,spec} %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/mgomp/
mv -f %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/*.a %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/
mv -f %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/mgomp/*.a %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/mgomp/
find %{buildroot}%{_prefix}/lib/gcc/nvptx-none %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none \
     %{buildroot}%{_prefix}/nvptx-none/lib -name \*.la | xargs rm
cd ..
rm -f newlib
%endif

cd obj-%{gcc_target_platform}

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
%if %{build_ada}
chmod 644 %{buildroot}%{_infodir}/gnat*
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}

# fix some things
ln -sf gcc %{buildroot}%{_prefix}/bin/cc
rm -f %{buildroot}%{_prefix}/lib/cpp
ln -sf ../bin/cpp %{buildroot}/%{_prefix}/lib/cpp
ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
ln -sf gcc %{buildroot}%{_prefix}/bin/gnatgcc
mkdir -p %{buildroot}%{_fmoddir}

%if %{build_go}
mv %{buildroot}%{_prefix}/bin/go{,.gcc}
mv %{buildroot}%{_prefix}/bin/gofmt{,.gcc}
ln -sf /etc/alternatives/go %{buildroot}%{_prefix}/bin/go
ln -sf /etc/alternatives/gofmt %{buildroot}%{_prefix}/bin/gofmt
%endif

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/*.h.gch dirs
# 1) there is no bits/*.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/*.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
cp -r -p $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}/man3
cp -r -p $libstdcxx_doc_builddir/man/man3/* %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

%ifarch sparcv9 sparc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc ppc64 ppc64p7
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

FULLLSUBDIR=
%ifarch sparcv9 ppc
FULLLSUBDIR=lib32
%endif
%ifarch sparc64 ppc64 ppc64p7
FULLLSUBDIR=lib64
%endif
if [ -n "$FULLLSUBDIR" ]; then
  FULLLPATH=$FULLPATH/$FULLLSUBDIR
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f

mv %{buildroot}%{_prefix}/%{_lib}/libgfortran.spec $FULLPATH/
%if %{build_d}
mv %{buildroot}%{_prefix}/%{_lib}/libgphobos.spec $FULLPATH/
%endif
%if %{build_libitm}
mv %{buildroot}%{_prefix}/%{_lib}/libitm.spec $FULLPATH/
%endif
%if %{build_libasan}
mv %{buildroot}%{_prefix}/%{_lib}/libsanitizer.spec $FULLPATH/
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_major}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
%ifarch %{ix86} x86_64 ppc ppc64 ppc64p7 ppc64le %{arm} aarch64 riscv64
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( /%{_lib}/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%else
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%endif
%ifarch sparcv9 ppc
%ifarch ppc
rm -f $FULLPATH/64/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -m64 -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( /lib64/libgcc_s.so.1 libgcc.a )' > $FULLPATH/64/libgcc_s.so
%else
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%endif
%ifarch %{multilib_64_archs}
%ifarch x86_64 ppc64 ppc64p7
rm -f $FULLPATH/64/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -m32 -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%else
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so %{buildroot}%{_prefix}/%{_lib}/
mv -f $FULLPATH/adalib/libgnat-*.so %{buildroot}%{_prefix}/%{_lib}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

mkdir -p %{buildroot}%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -P -dD -xc /dev/null | grep '__LONG_MAX__.*\(2147483647\|0x7fffffff\($\|[LU]\)\)'; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_prefix}/libexec/getconf/default
fi

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
pushd ../libstdc++-v3/python
for i in `find . -name \*.py`; do
  touch -r $i %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/$i
done
touch -r hook.in %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc++*gdb.py
popd
for f in `find %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/ \
	       %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/ -name \*.py`; do
  r=${f/$RPM_BUILD_ROOT/}
  %{__python3} -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
  %{__python3} -O -c 'import py_compile; py_compile.compile("'$f'", dfile="'$r'")'
done

rm -f $FULLEPATH/libgccjit.so
cp -a objlibgccjit/gcc/libgccjit.so* %{buildroot}%{_prefix}/%{_lib}/
cp -a ../gcc/jit/libgccjit*.h %{buildroot}%{_prefix}/include/
/usr/bin/install -c -m 644 objlibgccjit/gcc/doc/libgccjit.info %{buildroot}/%{_infodir}/
gzip -9 %{buildroot}/%{_infodir}/libgccjit.info

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
%if %{build_objc}
ln -sf ../../../libobjc.so.4 libobjc.so
%endif
ln -sf ../../../libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../libgfortran.so.5.* libgfortran.so
ln -sf ../../../libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../libgo.so.16.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../libquadmath.so.0.* libquadmath.so
%endif
%if %{build_d}
ln -sf ../../../libgdruntime.so.1.* libgdruntime.so
ln -sf ../../../libgphobos.so.1.* libgphobos.so
%endif
%if %{build_libitm}
ln -sf ../../../libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../libasan.so.6.* libasan.so
mv ../../../libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../libubsan.so.1.* libubsan.so
%endif
else
%if %{build_objc}
ln -sf ../../../../%{_lib}/libobjc.so.4 libobjc.so
%endif
ln -sf ../../../../%{_lib}/libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../../%{_lib}/libgfortran.so.5.* libgfortran.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../../%{_lib}/libgo.so.16.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../../%{_lib}/libquadmath.so.0.* libquadmath.so
%endif
%if %{build_d}
ln -sf ../../../../%{_lib}/libgdruntime.so.1.* libgdruntime.so
ln -sf ../../../../%{_lib}/libgphobos.so.1.* libgphobos.so
%endif
%if %{build_libitm}
ln -sf ../../../../%{_lib}/libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../../%{_lib}/libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../../%{_lib}/libasan.so.6.* libasan.so
mv ../../../../%{_lib}/libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../../%{_lib}/libubsan.so.1.* libubsan.so
%endif
%if %{build_libtsan}
rm -f libtsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/libtsan.so.0.* | sed 's,^.*libt,libt,'`' )' > libtsan.so
mv ../../../../%{_lib}/libtsan_preinit.o libtsan_preinit.o
%endif
%if %{build_liblsan}
rm -f liblsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/liblsan.so.0.* | sed 's,^.*libl,libl,'`' )' > liblsan.so
mv ../../../../%{_lib}/liblsan_preinit.o liblsan_preinit.o
%endif
fi
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++fs.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a $FULLLPATH/
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_d}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgdruntime.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgphobos.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_prefix}/%{_lib}/libitm.*a $FULLLPATH/
%endif
%if %{build_libatomic}
mv -f %{buildroot}%{_prefix}/%{_lib}/libatomic.*a $FULLLPATH/
%endif
%if %{build_libasan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan.*a $FULLLPATH/
%endif
%if %{build_libubsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libubsan.*a $FULLLPATH/
%endif
%if %{build_libtsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan.*a $FULLPATH/
%endif
%if %{build_liblsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/liblsan.*a $FULLPATH/
%endif
%if %{build_go}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgo.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgobegin.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgolibbegin.*a $FULLLPATH/
%endif

%if %{build_ada}
%ifarch sparcv9 ppc
rm -rf $FULLPATH/64/ada{include,lib}
%endif
%ifarch %{multilib_64_archs}
rm -rf $FULLPATH/32/ada{include,lib}
%endif
if [ "$FULLPATH" != "$FULLLPATH" ]; then
mv -f $FULLPATH/ada{include,lib} $FULLLPATH/
pushd $FULLLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../../libgnarl-*.so libgnarl-9.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-9.so
else
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl-9.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat-9.so
fi
popd
else
pushd $FULLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-9.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-9.so
else
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-9.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-9.so
fi
popd
fi
%endif

%ifarch sparcv9 ppc
%if %{build_objc}
ln -sf ../../../../../lib64/libobjc.so.4 64/libobjc.so
%endif
ln -sf ../`echo ../../../../lib/libstdc++.so.6.*[0-9] | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.5.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgo.so.16.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgo.so.16.* | sed 's,^.*libg,libg,'`' )' > 64/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 64/libquadmath.so
%endif
%if %{build_d}
rm -f libgdruntime.so libgphobos.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgdruntime.so.1.* | sed 's,^.*libg,libg,'`' )' > libgdruntime.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgdruntime.so.1.* | sed 's,^.*libg,libg,'`' )' > 64/libgdruntime.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgphobos.so.1.* | sed 's,^.*libg,libg,'`' )' > libgphobos.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgphobos.so.1.* | sed 's,^.*libg,libg,'`' )' > 64/libgphobos.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 64/libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > libatomic.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > 64/libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libasan.so.6.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libasan.so.6.* | sed 's,^.*liba,liba,'`' )' > 64/libasan.so
mv ../../../../lib64/libasan_preinit.o 64/libasan_preinit.o
%endif
%if %{build_libubsan}
rm -f libubsan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libubsan.so.1.* | sed 's,^.*libu,libu,'`' )' > libubsan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libubsan.so.1.* | sed 's,^.*libu,libu,'`' )' > 64/libubsan.so
%endif
ln -sf lib32/libgfortran.a libgfortran.a
ln -sf ../lib64/libgfortran.a 64/libgfortran.a
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/lib64/libobjc.*a 64/
%endif
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libstdc++fs.a libstdc++fs.a
ln -sf ../lib64/libstdc++fs.a 64/libstdc++fs.a
ln -sf lib32/libsupc++.a libsupc++.a
ln -sf ../lib64/libsupc++.a 64/libsupc++.a
%if %{build_libquadmath}
ln -sf lib32/libquadmath.a libquadmath.a
ln -sf ../lib64/libquadmath.a 64/libquadmath.a
%endif
%if %{build_d}
ln -sf lib32/libgdruntime.a libgdruntime.a
ln -sf ../lib64/libgdruntime.a 64/libgdruntime.a
ln -sf lib32/libgphobos.a libgphobos.a
ln -sf ../lib64/libgphobos.a 64/libgphobos.a
%endif
%if %{build_libitm}
ln -sf lib32/libitm.a libitm.a
ln -sf ../lib64/libitm.a 64/libitm.a
%endif
%if %{build_libatomic}
ln -sf lib32/libatomic.a libatomic.a
ln -sf ../lib64/libatomic.a 64/libatomic.a
%endif
%if %{build_libasan}
ln -sf lib32/libasan.a libasan.a
ln -sf ../lib64/libasan.a 64/libasan.a
%endif
%if %{build_libubsan}
ln -sf lib32/libubsan.a libubsan.a
ln -sf ../lib64/libubsan.a 64/libubsan.a
%endif
%if %{build_go}
ln -sf lib32/libgo.a libgo.a
ln -sf ../lib64/libgo.a 64/libgo.a
ln -sf lib32/libgobegin.a libgobegin.a
ln -sf ../lib64/libgobegin.a 64/libgobegin.a
ln -sf lib32/libgolibbegin.a libgolibbegin.a
ln -sf ../lib64/libgolibbegin.a 64/libgolibbegin.a
%endif
%if %{build_ada}
ln -sf lib32/adainclude adainclude
ln -sf ../lib64/adainclude 64/adainclude
ln -sf lib32/adalib adalib
ln -sf ../lib64/adalib 64/adalib
%endif
%endif
%ifarch %{multilib_64_archs}
mkdir -p 32
%if %{build_objc}
ln -sf ../../../../libobjc.so.4 32/libobjc.so
%endif
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.*[0-9] | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgfortran.so.5.* | sed s~/../lib64/~/~` 32/libgfortran.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgo.so.16.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgo.so.16.* | sed 's,^.*libg,libg,'`' )' > 32/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 32/libquadmath.so
%endif
%if %{build_d}
rm -f libgdruntime.so libgphobos.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgdruntime.so.1.* | sed 's,^.*libg,libg,'`' )' > libgdruntime.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgdruntime.so.1.* | sed 's,^.*libg,libg,'`' )' > 32/libgdruntime.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgphobos.so.1.* | sed 's,^.*libg,libg,'`' )' > libgphobos.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgphobos.so.1.* | sed 's,^.*libg,libg,'`' )' > 32/libgphobos.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 32/libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > libatomic.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > 32/libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libasan.so.6.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libasan.so.6.* | sed 's,^.*liba,liba,'`' )' > 32/libasan.so
mv ../../../../lib/libasan_preinit.o 32/libasan_preinit.o
%endif
%if %{build_libubsan}
rm -f libubsan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libubsan.so.1.* | sed 's,^.*libu,libu,'`' )' > libubsan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libubsan.so.1.* | sed 's,^.*libu,libu,'`' )' > 32/libubsan.so
%endif
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
%endif
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%endif
%ifarch sparc64 ppc64 ppc64p7
ln -sf ../lib32/libgfortran.a 32/libgfortran.a
ln -sf lib64/libgfortran.a libgfortran.a
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libstdc++fs.a 32/libstdc++fs.a
ln -sf lib64/libstdc++fs.a libstdc++fs.a
ln -sf ../lib32/libsupc++.a 32/libsupc++.a
ln -sf lib64/libsupc++.a libsupc++.a
%if %{build_libquadmath}
ln -sf ../lib32/libquadmath.a 32/libquadmath.a
ln -sf lib64/libquadmath.a libquadmath.a
%endif
%if %{build_d}
ln -sf ../lib32/libgdruntime.a 32/libgdruntime.a
ln -sf lib64/libgdruntime.a libgdruntime.a
ln -sf ../lib32/libgphobos.a 32/libgphobos.a
ln -sf lib64/libgphobos.a libgphobos.a
%endif
%if %{build_libitm}
ln -sf ../lib32/libitm.a 32/libitm.a
ln -sf lib64/libitm.a libitm.a
%endif
%if %{build_libatomic}
ln -sf ../lib32/libatomic.a 32/libatomic.a
ln -sf lib64/libatomic.a libatomic.a
%endif
%if %{build_libasan}
ln -sf ../lib32/libasan.a 32/libasan.a
ln -sf lib64/libasan.a libasan.a
%endif
%if %{build_libubsan}
ln -sf ../lib32/libubsan.a 32/libubsan.a
ln -sf lib64/libubsan.a libubsan.a
%endif
%if %{build_go}
ln -sf ../lib32/libgo.a 32/libgo.a
ln -sf lib64/libgo.a libgo.a
ln -sf ../lib32/libgobegin.a 32/libgobegin.a
ln -sf lib64/libgobegin.a libgobegin.a
ln -sf ../lib32/libgolibbegin.a 32/libgolibbegin.a
ln -sf lib64/libgolibbegin.a libgolibbegin.a
%endif
%if %{build_ada}
ln -sf ../lib32/adainclude 32/adainclude
ln -sf lib64/adainclude adainclude
ln -sf ../lib32/adalib 32/adalib
ln -sf lib64/adalib adalib
%endif
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgfortran.a 32/libgfortran.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++fs.a 32/libstdc++fs.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libsupc++.a 32/libsupc++.a
%if %{build_libquadmath}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libquadmath.a 32/libquadmath.a
%endif
%if %{build_d}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgdruntime.a 32/libgdruntime.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgphobos.a 32/libgphobos.a
%endif
%if %{build_libitm}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libitm.a 32/libitm.a
%endif
%if %{build_libatomic}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libatomic.a 32/libatomic.a
%endif
%if %{build_libasan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libasan.a 32/libasan.a
%endif
%if %{build_libubsan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libubsan.a 32/libubsan.a
%endif
%if %{build_go}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgo.a 32/libgo.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgobegin.a 32/libgobegin.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgolibbegin.a 32/libgolibbegin.a
%endif
%if %{build_ada}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/adainclude 32/adainclude
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/adalib 32/adalib
%endif
%endif
%endif

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if 0%{?_enable_debug_packages}
for d in . $FULLLSUBDIR; do
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/$d
  for f in `find $d -maxdepth 1 -a \
		\( -name libasan.a -o -name libatomic.a \
		-o -name libcaf_single.a \
		-o -name libgcc.a -o -name libgcc_eh.a \
		-o -name libgcov.a -o -name libgfortran.a \
		-o -name libgo.a -o -name libgobegin.a \
		-o -name libgolibbegin.a -o -name libgomp.a \
		-o -name libitm.a -o -name liblsan.a \
		-o -name libobjc.a -o -name libgdruntime.a -o -name libgphobos.a \
		-o -name libquadmath.a -o -name libstdc++.a \
		-o -name libstdc++fs.a -o -name libsupc++.a \
		-o -name libtsan.a -o -name libubsan.a \) -a -type f`; do
    cp -a $f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/$d/
  done
done
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
		    -o -name libgcc.a -o -name libgcov.a -o -name libquadmath.a \
		    -o -name libgdruntime.a -o -name libgphobos.a \
		    -o -name libitm.a -o -name libgo.a -o -name libcaf\*.a \
		    -o -name libatomic.a -o -name libasan.a -o -name libtsan.a \
		    -o -name libubsan.a -o -name liblsan.a -o -name libcc1.a \) \
		 -a -type f`
popd
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.5.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcc1.so.0.*
%if %{build_libquadmath}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
%if %{build_d}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgdruntime.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgphobos.so.1.*
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libitm.so.1.*
%endif
%if %{build_libatomic}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1.*
%endif
%if %{build_libasan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libasan.so.6.*
%endif
%if %{build_libubsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libubsan.so.1.*
%endif
%if %{build_libtsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libtsan.so.0.*
%endif
%if %{build_liblsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/liblsan.so.0.*
%endif
%if %{build_go}
# Avoid stripping these libraries and binaries.
chmod 644 %{buildroot}%{_prefix}/%{_lib}/libgo.so.16.*
chmod 644 %{buildroot}%{_prefix}/bin/go.gcc
chmod 644 %{buildroot}%{_prefix}/bin/gofmt.gcc
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet
%endif
%if %{build_objc}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.4.*
%endif

%if %{build_ada}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnat*so*
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > %{buildroot}%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
cat > %{buildroot}%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
chmod 755 %{buildroot}%{_prefix}/bin/c?9

cd ..
%find_lang %{name}
%find_lang cpplib

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a} || :
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
rm -f %{buildroot}%{_prefix}/%{_lib}/libvtv* || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gfortran || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gccgo || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcj || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ar || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-nm || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ranlib || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gdc || :

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
rm -f %{buildroot}/lib/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%ifnarch sparc64 ppc64 ppc64p7
ln -sf %{multilib_32_arch}-%{_vendor}-%{_target_os} %{buildroot}%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
rm -f %{buildroot}/lib64/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib64/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%endif

rm -f %{buildroot}%{mandir}/man3/ffi*

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{_arch} > $FULLPATH/rpmver

# Add symlink to lto plugin in the binutils plugin directory.
%{__mkdir_p} %{buildroot}%{_libdir}/bfd-plugins/
ln -s ../../libexec/gcc/%{gcc_target_platform}/%{gcc_major}/liblto_plugin.so \
  %{buildroot}%{_libdir}/bfd-plugins/

%check
cd obj-%{gcc_target_platform}

# run the tests.
LC_ALL=C make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ \
%if 0%{?fedora} >= 20 || 0%{?rhel} > 7
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector-strong}'" || :
%else
     RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
%endif
if [ -f %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/annobin.so ]; then
  # Test whether current annobin plugin won't fail miserably with the newly built gcc.
  echo -e '#include <stdio.h>\nint main () { printf ("Hello, world!\\n"); return 0; }' > annobin-test.c
  echo -e '#include <iostream>\nint main () { std::cout << "Hello, world!" << std::endl; return 0; }' > annobin-test.C
  `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc` \
  -O2 -g -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS \
  -fexceptions -fstack-protector-strong -grecord-gcc-switches -o annobin-test{c,.c} \
  -Wl,-rpath,%{gcc_target_platform}/libgcc/ \
  -fplugin=%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/annobin.so \
  2> ANNOBINOUT1 || echo Annobin test 1 FAIL > ANNOBINOUT2;
  `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` \
  `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes` \
  -O2 -g -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS \
  -fexceptions -fstack-protector-strong -grecord-gcc-switches -o annobin-test{C,.C} \
  -Wl,-rpath,%{gcc_target_platform}/libgcc/:%{gcc_target_platform}/libstdc++-v3/src/.libs/ \
  -fplugin=%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/annobin.so \
  -B %{gcc_target_platform}/libstdc++-v3/src/.libs/ \
  2> ANNOBINOUT3 || echo Annobin test 2 FAIL > ANNOBINOUT4;
  [ -f ./annobin-testc ] || echo Annobin test 1 MISSING > ANNOBINOUT5;
  [ -f ./annobin-testc ] && \
  ( ./annobin-testc > ANNOBINRES1 2>&1 || echo Annobin test 1 RUNFAIL > ANNOBINOUT6 );
  [ -f ./annobin-testC ] || echo Annobin test 2 MISSING > ANNOBINOUT7;
  [ -f ./annobin-testC ] && \
  ( ./annobin-testC > ANNOBINRES2 2>&1 || echo Annobin test 2 RUNFAIL > ANNOBINOUT8 );
  cat ANNOBINOUT[1-8] > ANNOBINOUT
  touch ANNOBINRES1 ANNOBINRES2
  [ -s ANNOBINOUT ] && echo Annobin testing FAILed > ANNOBINRES
  cat ANNOBINOUT ANNOBINRES[12] >> ANNOBINRES
  rm -f ANNOBINOUT* ANNOBINRES[12] annobin-test{c,C}
fi
echo ====================TESTING=========================
( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
[ -f ANNOBINRES ] && cat ANNOBINRES
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | xz -9e \
  | uuencode testlogs-%{_target_platform}.tar.xz || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%post go
%{_sbindir}/update-alternatives --install \
  %{_prefix}/bin/go go %{_prefix}/bin/go.gcc 92 \
  --slave %{_prefix}/bin/gofmt gofmt %{_prefix}/bin/gofmt.gcc

%preun go
if [ $1 = 0 ]; then
  %{_sbindir}/update-alternatives --remove go %{_prefix}/bin/go.gcc
fi

# Because glibc Prereq's libgcc and /sbin/ldconfig
# comes from glibc, it might not exist yet when
# libgcc is installed
%post -n libgcc -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%postun -n libgcc -p <lua>
if posix.access ("/sbin/ldconfig", "x") then
  local pid = posix.fork ()
  if pid == 0 then
    posix.exec ("/sbin/ldconfig")
  elseif pid ~= -1 then
    posix.wait (pid)
  end
end

%ldconfig_scriptlets -n libstdc++

%ldconfig_scriptlets -n libobjc

%ldconfig_scriptlets -n libgfortran

%ldconfig_scriptlets -n libgphobos

%ldconfig_scriptlets -n libgnat

%ldconfig_scriptlets -n libgomp

%ldconfig_scriptlets gdb-plugin

%ldconfig_scriptlets -n libgccjit

%ldconfig_scriptlets -n libgquadmath

%ldconfig_scriptlets -n libitm

%ldconfig_scriptlets -n libatomic

%ldconfig_scriptlets -n libasan

%ldconfig_scriptlets -n libubsan

%ldconfig_scriptlets -n libtsan

%ldconfig_scriptlets -n liblsan

%ldconfig_scriptlets -n libgo

%files -f %{name}.lang
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%{_prefix}/bin/gcov-tool
%{_prefix}/bin/gcov-dump
%{_prefix}/bin/gcc-ar
%{_prefix}/bin/gcc-nm
%{_prefix}/bin/gcc-ranlib
%{_prefix}/bin/lto-dump
%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc64 ppc64p7
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc
%{_prefix}/bin/%{gcc_target_platform}-gcc-%{gcc_major}
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man1/gcov-tool.1*
%{_mandir}/man1/gcov-dump.1*
%{_mandir}/man1/lto-dump.1*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/liblto_plugin.so*
%{_libdir}/bfd-plugins/liblto_plugin.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/openacc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/acc_prof.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdatomic.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/gcov.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512cdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512erintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512fintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512pfintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/shaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cross-stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512dqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmavlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlbwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vldqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clflushoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clwbintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mwaitxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavecintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clzerointrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pkuintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx5124fmapsintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx5124vnniwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vpopcntdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sgxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/gfniintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cetintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cet.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmi2vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vnniintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vnnivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vaesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vpclmulqdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vpopcntdqvlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bitalgintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pconfigintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/wbnoinvdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/movdirintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/waitpkgintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cldemoteintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bf16vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bf16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/enqcmdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vp2intersectintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vp2intersectvlintrin.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ia64intrin.h
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vec_types.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmxlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amo.h
%endif
%ifarch %{arm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_cmse.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_fp16.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_bf16.h
%endif
%ifarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_fp16.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_bf16.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_sve.h
%endif
%ifarch sparc sparcv9 sparc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/visintrin.h
%endif
%ifarch s390 s390x
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/s390intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmxlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vecintrin.h
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sanitizer
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.so
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.spec
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsanitizer.spec
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libubsan.so
%endif
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libubsan.so
%endif
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.so
%endif
%else
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.so
%endif
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan_preinit.o
%endif
%if %{build_liblsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan_preinit.o
%endif
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* 
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files -n cpp -f cpplib.lang
%{_prefix}/lib/cpp
%{_prefix}/bin/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1

%files -n libgcc
/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
/%{_lib}/libgcc_s.so.1
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files c++
%{_prefix}/bin/%{gcc_target_platform}-*++
%{_prefix}/bin/g++
%{_prefix}/bin/c++
%{_mandir}/man1/g++.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1plus
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsupc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++
%{_prefix}/%{_lib}/libstdc++.so.6*
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
# Package symlink to keep compatibility
%ifarch riscv64
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/lp64d
%endif
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/__pycache__
%dir %{_prefix}/share/gcc-%{gcc_major}
%dir %{_prefix}/share/gcc-%{gcc_major}/python
%{_prefix}/share/gcc-%{gcc_major}/python/libstdcxx

%files -n libstdc++-devel
%dir %{_prefix}/include/c++
%{_prefix}/include/c++/%{gcc_major}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.so
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++fs.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++fs.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++fs.a
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%files -n libstdc++-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libsupc++.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libsupc++.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsupc++.a
%endif

%if %{build_libstdcxx_docs}
%files -n libstdc++-docs
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%if %{build_objc}
%files objc
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libobjc.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libobjc.so
%endif
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1objplus

%files -n libobjc
%{_prefix}/%{_lib}/libobjc.so.4*
%endif

%files gfortran
%{_prefix}/bin/gfortran
%{_prefix}/bin/f95
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ISO_Fortran_binding.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_arithmetic.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_exceptions.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_features.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcaf_single.a
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/finclude
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/finclude
%endif
%dir %{_fmoddir}
%doc rpm.doc/gfortran/*

%files -n libgfortran
%{_prefix}/%{_lib}/libgfortran.so.5*

%files -n libgfortran-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgfortran.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgfortran.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.a
%endif

%if %{build_d}
%files gdc
%{_prefix}/bin/gdc
%{_mandir}/man1/gdc.1*
%{_infodir}/gdc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/d
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/d21
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.spec
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgdruntime.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgphobos.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgdruntime.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgphobos.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgphobos.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgdruntime.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgphobos.so
%endif
%doc rpm.doc/gdc/*

%files -n libgphobos
%{_prefix}/%{_lib}/libgdruntime.so.1*
%{_prefix}/%{_lib}/libgphobos.so.1*
%doc rpm.doc/libphobos/*

%files -n libgphobos-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgphobos.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgphobos.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.a
%endif
%endif

%if %{build_ada}
%files gnat
%{_prefix}/bin/gnat
%{_prefix}/bin/gnat[^i]*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/ada_target_properties
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/ada_target_properties
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/ada_target_properties
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so

%files -n libgnat-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnarl.a
%endif

%files -n libgnat-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnarl.a
%endif
%endif

%files -n libgomp
%{_prefix}/%{_lib}/libgomp.so.1*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%if %{build_libquadmath}
%files -n libquadmath
%{_prefix}/%{_lib}/libquadmath.so.0*
%{_infodir}/libquadmath.info*
%{!?_licensedir:%global license %%doc}
%license rpm.doc/libquadmath/COPYING*

%files -n libquadmath-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.so
%endif
%doc rpm.doc/libquadmath/ChangeLog*

%files -n libquadmath-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libquadmath.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libquadmath.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.a
%endif
%endif

%if %{build_libitm}
%files -n libitm
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*

%files -n libitm-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
#%%{_prefix}/lib/gcc/%%{gcc_target_platform}/%%{gcc_major}/include/itm.h
#%%{_prefix}/lib/gcc/%%{gcc_target_platform}/%%{gcc_major}/include/itm_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.so
%endif
%doc rpm.doc/libitm/ChangeLog*

%files -n libitm-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libitm.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libitm.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.a
%endif
%endif

%if %{build_libatomic}
%files -n libatomic
%{_prefix}/%{_lib}/libatomic.so.1*

%files -n libatomic-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libatomic.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libatomic.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.a
%endif
%doc rpm.doc/changelogs/libatomic/ChangeLog*
%endif

%if %{build_libasan}
%files -n libasan
%{_prefix}/%{_lib}/libasan.so.6*

%files -n libasan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libasan.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libasan.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.a
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libubsan}
%files -n libubsan
%{_prefix}/%{_lib}/libubsan.so.1*

%files -n libubsan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libubsan.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libubsan.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.a
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libtsan}
%files -n libtsan
%{_prefix}/%{_lib}/libtsan.so.0*

%files -n libtsan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_liblsan}
%files -n liblsan
%{_prefix}/%{_lib}/liblsan.so.0*

%files -n liblsan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_go}
%files go
%ghost %{_prefix}/bin/go
%attr(755,root,root) %{_prefix}/bin/go.gcc
%{_prefix}/bin/gccgo
%ghost %{_prefix}/bin/gofmt
%attr(755,root,root) %{_prefix}/bin/gofmt.gcc
%{_mandir}/man1/gccgo.1*
%{_mandir}/man1/go.1*
%{_mandir}/man1/gofmt.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/go1
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgolibbegin.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgolibbegin.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgolibbegin.a
%endif
%doc rpm.doc/go/*

%files -n libgo
%attr(755,root,root) %{_prefix}/%{_lib}/libgo.so.16*
%doc rpm.doc/libgo/*

%files -n libgo-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/%{_lib}/go
%dir %{_prefix}/%{_lib}/go/%{gcc_major}
%{_prefix}/%{_lib}/go/%{gcc_major}/%{gcc_target_platform}
%ifarch %{multilib_64_archs}
%ifnarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/go
%dir %{_prefix}/lib/go/%{gcc_major}
%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgolibbegin.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgolibbegin.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.so
%endif

%files -n libgo-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgo.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgo.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.a
%endif
%endif

%files -n libgccjit
%{_prefix}/%{_lib}/libgccjit.so.*
%doc rpm.doc/changelogs/gcc/jit/ChangeLog*

%files -n libgccjit-devel
%{_prefix}/%{_lib}/libgccjit.so
%{_prefix}/include/libgccjit*.h
%{_infodir}/libgccjit.info*
%doc rpm.doc/libgccjit-devel/*
%doc gcc/jit/docs/examples

%files plugin-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gtype.state
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/include
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/plugin

%files gdb-plugin
%{_prefix}/%{_lib}/libcc1.so*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcc1plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcp1plugin.so*
%doc rpm.doc/changelogs/libcc1/ChangeLog*

%if %{build_offload_nvptx}
%files offload-nvptx
%{_prefix}/bin/nvptx-none-*
%{_prefix}/bin/%{gcc_target_platform}-accel-nvptx-none-gcc
%{_prefix}/bin/%{gcc_target_platform}-accel-nvptx-none-lto-dump
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel
%{_prefix}/lib/gcc/nvptx-none
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none
%dir %{_prefix}/nvptx-none
%{_prefix}/nvptx-none/bin
%{_prefix}/nvptx-none/include

%files -n libgomp-offload-nvptx
%{_prefix}/%{_lib}/libgomp-plugin-nvptx.so.*
%endif

%changelog
* Wed Aug 26 2020 Jakub Jelinek <jakub@redhat.com> 10.2.1-3
- update from releases/gcc-10 branch
  - PRs c++/95428, c++/96082, c++/96106, c++/96164, c++/96199, c++/96497,
	c/96545, c/96549, c/96571, d/96250, d/96254, d/96301, debug/96354,
	fortran/93553, fortran/96312, fortran/96486, ipa/95320, ipa/96291,
	ipa/96482, libstdc++/89760, libstdc++/95749, libstdc++/96303,
	libstdc++/96484, libstdc++/96718, lto/95362, lto/95548,
	middle-end/96426, middle-end/96459, target/93897, target/95450,
	target/96191, target/96243, target/96446, target/96493, target/96506,
	target/96525, target/96530, target/96536, target/96562, target/96682,
	tree-optimization/96483, tree-optimization/96535,
	tree-optimization/96722, tree-optimization/96730,
	tree-optimization/96758
- mangle some further symbols needed for debug info during early dwarf
  (#1862029, PR debug/96690)
- during %%check perform tests whether annobin is usable with the newly built
  compiler or whether it might need to be rebuilt
- disable graphite for ELN

* Tue Aug  4 2020 Jakub Jelinek <jakub@redhat.com> 10.2.1-2
- update from releases/gcc-10 branch
  - PRs c++/95591, c++/95599, c++/95823, c++/95824, c++/95895, c/96377,
	d/96140, fortran/89574, fortran/93567, fortran/93592, fortran/95585,
	fortran/95612, fortran/95980, fortran/96018, fortran/96086,
	fortran/96220, fortran/96319, lto/45375, middle-end/96335,
	target/95435, target/96190, target/96236, target/96260, target/96402,
	tree-optimization/96058
- emit debug info for C/C++ external function declarations used in the TU
  (PR debug/96383)
- discard SHN_UNDEF global symbols from LTO debuginfo (PR lto/96385)
- strip also -flto=auto from optflags

* Thu Jul 23 2020 Jakub Jelinek <jakub@redhat.com> 10.2.1-1
- update from releases/gcc-10 branch
  - GCC 10.2 release
  - PRs bootstrap/94998, c++/90916, c++/95477, c++/95505, c++/95518,
	c++/95519, c++/95711, c++/95719, c++/95736, c++/95789, c++/95813,
	c++/95976, c++/96052, c++/96063, c++/96077, c++/96104, c++/96105,
	c++/96179, c/95141, d/95173, d/95250, debug/95343, fortran/71706,
	fortran/88379, fortran/93337, fortran/95340, fortran/95366,
	fortran/95587, fortran/95687, fortran/95688, fortran/95689,
	fortran/95707, fortran/95708, fortran/95709, fortran/95743,
	fortran/95812, fortran/95826, fortran/95827, fortran/95828,
	fortran/95829, fortran/95880, fortran/95881, fortran/95978,
	ipa/12345, ipa/93223, ipa/96040, ipa/96130, libstdc++/91153,
	libstdc++/91807, libstdc++/94087, libstdc++/94627, libstdc++/94936,
	libstdc++/95282, libstdc++/95851, libstdc++/95915, lto/91576,
	lto/95604, middle-end/94600, middle-end/94964, middle-end/95114,
	middle-end/95118, middle-end/95270, middle-end/95493,
	middle-end/95690, middle-end/95810, middle-end/95903,
	middle-end/96194, target/12345, target/93224, target/93492,
	target/94791, target/94891, target/95018, target/95105, target/95347,
	target/95581, target/95683, target/95713, target/95726, target/95874,
	target/96001, target/96125, target/96174, testsuite/96180,
	tree-optimization/90838, tree-optimization/94969,
	tree-optimization/95049, tree-optimization/95110,
	tree-optimization/95133, tree-optimization/95308,
	tree-optimization/95487, tree-optimization/95638,
	tree-optimization/95717, tree-optimization/95804,
	tree-optimization/95857, tree-optimization/96075,
	tree-optimization/96133, tree-optimization/96146
  - disable s390x multilibs also for ELN
  - disable -flto in %%{optflags}, lto bootstrap will be enabled the GCC way
    later

* Thu Jun 18 2020 Jakub Jelinek <jakub@redhat.com> 10.1.1-2
- update from releases/gcc-10 branch
  - PRs c++/90212, c++/90479, c++/90915, c++/91529, c++/92103, c++/92633,
	c++/92652, c++/92838, c++/93310, c++/93467, c++/93698, c++/93822,
	c++/94128, c++/94817, c++/94829, c++/94885, c++/94937, c++/94955,
	c++/95003, c++/95020, c++/95050, c++/95066, c++/95087, c++/95137,
	c++/95158, c++/95181, c++/95197, c++/95222, c++/95241, c++/95319,
	c++/95328, c++/95344, c++/95345, c++/95346, c++/95350, c++/95371,
	c++/95386, c++/95440, c++/95508, c++/95560, c++/95562, c/95040,
	c/95580, d/94970, d/95166, d/95167, d/95168, debug/95080,
	fortran/39695, fortran/50392, fortran/59107, fortran/92993,
	fortran/93366, fortran/93497, fortran/94109, fortran/94361,
	fortran/94397, fortran/94672, fortran/95088, fortran/95090,
	fortran/95091, fortran/95106, fortran/95373, fortran/95500,
	fortran/95503, fortran/95530, fortran/95537, fortran/95544,
	fortran/95611, gcov-profile/95332, ipa/94947, ipa/95113,
	libfortran/95104, libfortran/95119, libfortran/95191,
	libfortran/95390, libgomp/92854, libstdc++/77691, libstdc++/92894,
	libstdc++/93983, libstdc++/94906, libstdc++/94933, libstdc++/95289,
	libstdc++/95322, libstdc++/95578, lto/94848, lto/95190,
	middle-end/94940, middle-end/95108, middle-end/95551,
	middle-end/95622, sanitizer/94910, sanitizer/95634, target/91695,
	target/94591, target/94735, target/94959, target/95169, target/95212,
	target/95220, target/95255, target/95258, target/95355, target/95420,
	target/95525, target/95528, testsuite/95361, testsuite/95575,
	web/95380
- correct instructions for creation of newlib tarball, filter out sun-rpc
  licensed code that is never used during the package build

* Mon May 11 2020 Tom Stellard <tstellar@redhat.com>
- add symlink to liblto_plugin.so in /usr/lib/bfd-plugins

* Thu May  7 2020 Jakub Jelinek <jakub@redhat.com> 10.1.1-1
- update from releases/gcc-10 branch
  - GCC 10.1.0 release
  - PRs bootstrap/94918, c++/94907, c++/94938, c++/94946, c++/94951, c/94842,
	c/94968, libstdc++/94901, middle-end/94941, rtl-optimization/94873,
	target/94942, target/94950

* Sat May  2 2020 Jakub Jelinek <jakub@redhat.com> 10.0.1-0.14
- use libgcc_s.so linker script also on aarch64 and riscv64 (#1830472)

* Fri May  1 2020 Jakub Jelinek <jakub@redhat.com> 10.0.1-0.13
- update from trunk and releases/gcc-10 branch
  - GCC 10.1-rc1
  - PRs analyzer/94447, analyzer/94639, analyzer/94732, analyzer/94754,
	analyzer/94816, bootstrap/94739, c++/79585, c++/90320, c++/90448,
	c++/90750, c++/93807, c++/94288, c++/94383, c++/94505, c++/94510,
	c++/94546, c++/94549, c++/94583, c++/94592, c++/94597, c++/94628,
	c++/94645, c++/94661, c++/94682, c++/94701, c++/94719, c++/94733,
	c++/94742, c++/94752, c++/94759, c++/94760, c++/94772, c++/94775,
	c++/94808, c++/94819, c++/94827, c++/94830, c++/94879, c++/94883,
	c++/94886, c/94641, c/94686, c/94705, c/94755, d/89418, d/94777,
	d/94825, demangler/94797, driver/90983, fortran/90350, fortran/93956,
	fortran/94578, fortran/94709, fortran/94737, fortran/94769,
	fortran/94788, ipa/94856, libfortran/25830, libfortran/94586,
	libfortran/94694, libstdc++/89510, libstdc++/90415, libstdc++/91480,
	libstdc++/92156, libstdc++/94831, libstdc++/94854, lto/94659,
	lto/94822, middle-end/92830, middle-end/93488, middle-end/94647,
	middle-end/94724, rtl-optimization/94708, rtl-optimization/94740,
	target/57002, target/91518, target/92713, target/93654, target/94248,
	target/94279, target/94282, target/94383, target/94514, target/94515,
	target/94577, target/94613, target/94622, target/94668, target/94678,
	target/94697, target/94704, target/94706, target/94707, target/94710,
	target/94711, target/94748, target/94780, target/94812, target/94820,
	target/94826, target/94832, testsuite/94712, translation/94698,
	tree-optimization/89430, tree-optimization/94683,
	tree-optimization/94700, tree-optimization/94717,
	tree-optimization/94727, tree-optimization/94734,
	tree-optimization/94774, tree-optimization/94784,
	tree-optimization/94809

* Mon Apr 20 2020 Jakub Jelinek <jakub@redhat.com> 10.0.1-0.12
- update from trunk
  - PRs analyzer/94378, bootstrap/89494, bootstrap/92008, c++/67825,
	c++/79937, c++/85278, c++/86327, c++/88754, c++/90711, c++/90996,
	c++/91377, c++/91966, c++/92010, c++/92187, c++/92878, c++/93207,
	c++/93211, c++/93790, c++/94034, c++/94149, c++/94155, c++/94205,
	c++/94219, c++/94252, c++/94306, c++/94314, c++/94325, c++/94359,
	c++/94385, c++/94426, c++/94453, c++/94454, c++/94462, c++/94470,
	c++/94475, c++/94477, c++/94478, c++/94480, c++/94481, c++/94483,
	c++/94507, c++/94512, c++/94521, c++/94523, c++/94528, c++/94571,
	c++/94588, c++/94608, c++/94632, c/92326, c/94392, c/94593, d/90136,
	d/94304, d/94305, d/94315, d/94321, d/94424, d/94425, d/94609,
	debug/94439, debug/94441, debug/94450, debug/94459, debug/94495,
	driver/94381, fortran/57129, fortran/85982, fortran/87644,
	fortran/87923, fortran/91800, fortran/93364, fortran/93498,
	fortran/93500, fortran/93522, fortran/93686, fortran/93871,
	fortran/94030, fortran/94090, fortran/94091, fortran/94192,
	fortran/94246, fortran/94347, fortran/94348, fortran/94386,
	gcov-profile/93401, gcov-profile/94570, go/94607, ipa/92676,
	ipa/93621, ipa/93940, ipa/94363, ipa/94434, ipa/94445, ipa/94582,
	libgcc/94513, libgomp/92843, libstdc++/93960, libstdc++/94498,
	libstdc++/94520, libstdc++/94562, libstdc++/94565, lto/94612,
	middle-end/89433, middle-end/93465, middle-end/94412,
	middle-end/94423, middle-end/94436, middle-end/94465,
	middle-end/94479, middle-end/94526, middle-end/94539,
	middle-end/94614, middle-end/94635, objc/94637, other/94629,
	rtl-optimization/84169, rtl-optimization/87716,
	rtl-optimization/93946, rtl-optimization/93974,
	rtl-optimization/94123, rtl-optimization/94291,
	rtl-optimization/94344, rtl-optimization/94468,
	rtl-optimization/94516, rtl-optimization/94605,
	rtl-optimization/94618, target/93053, target/94317, target/94368,
	target/94396, target/94417, target/94420, target/94435, target/94438,
	target/94460, target/94467, target/94488, target/94494, target/94500,
	target/94509, target/94530, target/94542, target/94551, target/94556,
	target/94561, target/94567, target/94584, target/94603, target/94606,
	testsuite/93369, testsuite/94079, testsuite/94402, testsuite/94533,
	tree-optimization/89713, tree-optimization/91322,
	tree-optimization/93674, tree-optimization/94043,
	tree-optimization/94398, tree-optimization/94401,
	tree-optimization/94403, tree-optimization/94443,
	tree-optimization/94482, tree-optimization/94524,
	tree-optimization/94573, tree-optimization/94574,
	tree-optimization/94598, tree-optimization/94621

* Sat Mar 28 2020 Jakub Jelinek <jakub@redhat.com> 10.0.1-0.11
- update from trunk
  - PRs c++/81349, c++/84733, c++/93810, c++/93824, c++/94057, c++/94078,
	c++/94098, c++/94257, c++/94265, c++/94272, c++/94319, c++/94326,
	c++/94336, c++/94339, c++/94346, c/93573, debug/94273, debug/94281,
	debug/94296, debug/94323, fortran/93363, fortran/93957, ipa/94271,
	lto/94259, middle-end/94004, rtl-optimization/92264, target/94145,
	target/94220, target/94292, testsuite/94334, tree-optimization/90332,
	tree-optimization/94131, tree-optimization/94269,
	tree-optimization/94329, tree-optimization/94352
- fix x86 vec_extract_{lo,hi}*_mask AVX512* patterns (PR target/93069)
- fix x86 *one_cmpl*2* AVX512* patterns (PR target/94343)
- add BuildRequires: libzstd-devel

* Wed Mar 25 2020 Jakub Jelinek <jakub@redhat.com> 10.0.1-0.10
- update from trunk
  - PRs analyzer/94047, analyzer/94099, analyzer/94105, c++/67960, c++/69694,
	c++/90995, c++/91759, c++/91993, c++/92068, c++/92909, c++/93248,
	c++/93596, c++/93805, c++/93931, c++/94044, c++/94066, c++/94147,
	c++/94175, c++/94186, c++/94190, c++/94197, c++/94223, c/94040,
	c/94172, c/94179, c/94239, d/92216, d/92309, d/92792, d/93038,
	d/94240, debug/93751, debug/94167, debug/94277, debug/94280,
	debug/94283, debug/94285, fortran/93365, fortran/93484, fortran/93600,
	gcov-profile/94029, ipa/92372, ipa/92799, ipa/93347, ipa/94202,
	ipa/94217, ipa/94232, ipa/94245, ipa/94250, libgomp/81689,
	libgomp/94251, libstdc++/93245, libstdc++/94033, libstdc++/94199,
	libstdc++/94203, libstdc++/94242, lto/91027, lto/94157, lto/94249,
	middle-end/92071, middle-end/93566, middle-end/94072,
	middle-end/94120, middle-end/94188, middle-end/94189,
	middle-end/94206, middle-end/94216, middle-end/94233,
	middle-end/94303, rtl-optimization/90275, rtl-optimization/92303,
	rtl-optimization/94042, rtl-optimization/94052,
	rtl-optimization/94119, rtl-optimization/94148, target/92379,
	target/93694, target/94052, target/94144, target/94154, target/94176,
	target/94185, target/94201, target/94238, target/94286,
	testsuite/93935, tree-optimization/93435, tree-optimization/94103,
	tree-optimization/94125, tree-optimization/94163,
	tree-optimization/94166, tree-optimization/94187,
	tree-optimization/94211, tree-optimization/94224,
	tree-optimization/94261, tree-optimization/94266,
	tree-optimization/94300
- fix ICE in final_scan_insn_1 on i686 with vzeroupper (#1816760,
  PR target/94308)
- fix ppc64* hang with dfp (PR target/94254)

* Wed Mar 11 2020 Jakub Jelinek <jakub@redhat.com> 10.0.1-0.9
- update from trunk
  - PRs ada/91100, analyzer/93032, analyzer/93388, analyzer/93692,
	analyzer/93774, analyzer/93775, analyzer/93777, analyzer/93778,
	analyzer/93779, analyzer/93899, analyzer/93947, analyzer/93950,
	analyzer/93959, analyzer/93993, analyzer/94028, bootstrap/93962,
	c++/52320, c++/66139, c++/90432, c++/90467, c++/90505, c++/90938,
	c++/91465, c++/92031, c++/92721, c++/93169, c++/93676, c++/93712,
	c++/93729, c++/93789, c++/93801, c++/93803, c++/93804, c++/93817,
	c++/93862, c++/93869, c++/93870, c++/93882, c++/93901, c++/93905,
	c++/93907, c++/93922, c++/93933, c++/93956, c++/93958, c++/93998,
	c++/94027, c++/94041, c++/94068, c++/94074, c++/94117, c++/94124,
	c/86134, c/93577, c/93812, c/93858, c/93886, c/93887, c/93949,
	debug/93888, driver/47785, driver/93796, fortran/92785, fortran/92959,
	fortran/92976, fortran/93486, fortran/93552, fortran/93580,
	fortran/93581, fortran/93599, fortran/93601, fortran/93603,
	fortran/93604, fortran/93714, fortran/93792, fortran/93825,
	fortran/93835, fortran/93889, fortran/93890, gcov-profile/93753,
	inline-asm/94095, ipa/92518, ipa/92548, ipa/92924, ipa/93583,
	ipa/93707, ipa/93760, ipa/93797, libstdc++/92546, libstdc++/93244,
	libstdc++/93818, libstdc++/93872, libstdc++/93884, libstdc++/93936,
	libstdc++/93972, libstdc++/93978, libstdc++/94013, libstdc++/94017,
	libstdc++/94051, libstdc++/94063, libstdc++/94069, lto/78353,
	middle-end/81401, middle-end/92152, middle-end/93399,
	middle-end/93829, middle-end/93843, middle-end/93874,
	middle-end/93926, middle-end/93961, middle-end/94111, other/55930,
	other/93756, other/93912, other/93965, rtl-optimization/93564,
	rtl-optimization/93996, rtl-optimization/94002,
	rtl-optimization/94045, rtl-optimization/PR92989, sanitizer/93731,
	target/26877, target/87560, target/87612, target/89229, target/89346,
	target/90311, target/90763, target/91276, target/91598, target/93047,
	target/93658, target/93709, target/93743, target/93800, target/93828,
	target/93860, target/93913, target/93932, target/93937, target/93995,
	target/93997, target/94046, target/94065, target/94088, target/94121,
	target/94134, testsuite/91797, testsuite/91799, testsuite/94019,
	testsuite/94023, translation/93755, translation/93759,
	translation/93830, translation/93831, translation/93838,
	translation/93841, translation/93864, tree-optimization/90883,
	tree-optimization/91890, tree-optimization/92128,
	tree-optimization/92982, tree-optimization/93508,
	tree-optimization/93586, tree-optimization/93667,
	tree-optimization/93767, tree-optimization/93776,
	tree-optimization/93780, tree-optimization/93820,
	tree-optimization/93845, tree-optimization/93868,
	tree-optimization/93927, tree-optimization/93945,
	tree-optimization/93946, tree-optimization/93953,
	tree-optimization/93964, tree-optimization/93986,
	tree-optimization/94001, tree-optimization/94114
  - fix ICE on rotate with -Wconversion (#1810941, PR c++/94067)
  - fix -fcf-protection -flto -g interaction (#1808484, PR lto/93966)
  - fix git miscompilation on s390x with -O2 -march=zEC12 -mtune=z13
    (#1799408, PR rtl-optimization/93908)
  - fix ICE in in propagate_vals_across_arith_jfunc (#1806466, PR ipa/93763)
  - ARM ABI alignment fix for classes derived from user aligned empty
    bases (PR c++/94050)
- strlen pass fixes (PR tree-optimization/94015)
- fix {memset,memcpy,memmove,strncpy} head trimming if the result is used
  (PR tree-optimization/94130)
- drop python2-devel Requires

* Sun Feb 16 2020 Jakub Jelinek <jakub@redhat.com> 10.0.1-0.8
- update from trunk
  - PRs analyzer/93212, analyzer/93288, analyzer/93350, analyzer/93356,
	analyzer/93373, analyzer/93374, analyzer/93379, analyzer/93405,
	analyzer/93438, analyzer/93457, analyzer/93543, analyzer/93544,
	analyzer/93546, analyzer/93547, analyzer/93647, analyzer/93649,
	analyzer/93657, analyzer/93659, analyzer/93669, c++/14179, c++/61414,
	c++/66477, c++/69448, c++/80471, c++/86216, c++/86917, c++/88256,
	c++/88819, c++/89404, c++/90691, c++/90951, c++/91953, c++/92003,
	c++/92517, c++/92556, c++/92583, c++/92593, c++/92654, c++/92717,
	c++/92947, c++/93140, c++/93458, c++/93530, c++/93549, c++/93551,
	c++/93557, c++/93559, c++/93597, c++/93618, c++/93633, c++/93643,
	c++/93650, c++/93675, c++/93684, c++/93710, c++/93713, c/87488,
	c/88660, c/93576, c/93640, fortran/83113, fortran/92305,
	fortran/93427, fortran/93462, fortran/93541, gcov-profile/91971,
	gcov-profile/93466, ipa/93203, libgcc/85334, libgomp/93481,
	libgomp/93515, libstdc++/79193, libstdc++/88999, libstdc++/92906,
	libstdc++/93562, lto/93489, middle-end/90648, middle-end/93519,
	middle-end/93555, middle-end/93646, middle-end/93663, other/93168,
	other/93641, preprocessor/92319, preprocessor/93545,
	rtl-optimization/91333, rtl-optimization/91838,
	rtl-optimization/93561, rtl-optimization/93565, target/58218,
	target/65782, target/85667, target/87763, target/91052, target/91816,
	target/91913, target/91927, target/92190, target/93122, target/93136,
	target/93300, target/93372, target/93532, target/93533, target/93548,
	target/93568, target/93569, target/93594, target/93611, target/93615,
	target/93637, target/93656, target/93670, target/93673, target/93696,
	target/93704, target/93724, testsuite/92177, testsuite/93697,
	testsuite/93717, tree-optimization/91123, tree-optimization/92819,
	tree-optimization/93516, tree-optimization/93538,
	tree-optimization/93582, tree-optimization/93661,
	tree-optimization/93662, tree-optimization/93683,
	tree-optimization/93744

* Thu Jan 30 2020 Jakub Jelinek <jakub@redhat.com> 10.0.1-0.7
- update from trunk
  - PRs analyzer/93276, analyzer/93291, analyzer/93349, analyzer/93450,
	analyzer/93451, bootstrap/93409, c++/60503, c++/82521, c++/88092,
	c++/89357, c++/89640, c++/90333, c++/90338, c++/90546, c++/90731,
	c++/90966, c++/90992, c++/91118, c++/91754, c++/91826, c++/92440,
	c++/92601, c++/92948, c++/93442, c++/93443, c++/93477, driver/91220,
	fortran/85781, fortran/87103, fortran/92123, fortran/93025,
	fortran/93461, fortran/93463, fortran/93464, fortran/93473,
	gcov-profile/93403, libstdc++/92895, libstdc++/93325, libstdc++/93426,
	libstdc++/93470, libstdc++/93478, libstdc++/93479, middle-end/92323,
	middle-end/93437, middle-end/93505, rtl-optimization/87763,
	rtl-optimization/92989, rtl-optimization/93170,
	rtl-optimization/93272, sanitizer/93436, target/91399, target/91461,
	target/91824, target/92822, target/93221, target/93274, target/93418,
	target/93494, testsuite/71727, testsuite/91171, testsuite/93393,
	testsuite/93460, tree-optimization/89689, tree-optimization/92706,
	tree-optimization/92822, tree-optimization/93397,
	tree-optimization/93428, tree-optimization/93434,
	tree-optimization/93439, tree-optimization/93454
  - LTO fix for *.localalias aliases (#1795575, PR lto/93384)
  - __has_include{,_next} fix (#1795633, PR preprocessor/93452)

* Sun Jan 26 2020 Jakub Jelinek <jakub@redhat.com> 10.0.1-0.6
- update from trunk
  - PRs analyzer/93367, c++/90997, c++/92852, c++/93279, c++/93299, c++/93377,
	c++/93400, c++/93414, inline-asm/93027, ipa/93166, target/13721,
	target/92269, target/93395, target/93412, target/93430,
	translation/90162, tree-optimization/92788
- temporarily disable broken strcmp optimization (PR tree-optimization/92765)
- riscv64 tweaks from David Abdurachmanov (#1794343)

* Thu Jan 23 2020 Jakub Jelinek <jakub@redhat.com> 10.0.1-0.5
- update from trunk
  - PRs analyzer/93307, analyzer/93316, analyzer/93352, analyzer/93375,
	analyzer/93378, analyzer/93382, c++/40752, c++/60855, c++/90732,
	c++/91476, c++/92804, c++/92907, c++/93324, c++/93331, c++/93345,
	c/84919, c/93348, fortran/93329, ipa/93315, libstdc++/91947,
	rtl-optimization/93124, rtl-optimization/93402, target/91298,
	target/92424, target/9311, target/93119, target/93333, target/93335,
	target/93341, target/93346, target/93376, testsuite/93391,
	tree-optimization/92924, tree-optimization/93381
  - fix ICE in nothrow_spec_p (#1794094, c++/93345)

* Tue Jan 21 2020 Jakub Jelinek <jakub@redhat.com> 10.0.1-0.4
- update from trunk
  - PRs c++/33799, c++/92536, debug/92763, fortran/44960, fortran/93309,
	lto/93318, middle-end/93194, middle-end/93242, preprocessor/80005,
	target/93073, target/93304, target/93319, testsuite/92829,
	tree-opt/93321, tree-optimization/92328, tree-optimization/93094,
	tree-optimization/93199
- add arm_bf16.h and arm_sve.h to arm and arm/aarch64 (#1793471)

* Sat Jan 18 2020 Jakub Jelinek <jakub@redhat.com> 10.0.1-0.3
- new package
