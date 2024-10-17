%define major 23
%define libslurm %mklibname slurm %{major}

Name:    slurm
Version: 2.4.3
Release: 3
Summary: Simple Linux Utility for Resource Management
License: GPLv2
Group: System/Cluster
Source0: http://www.schedmd.com/download/latest/slurm-%{version}.tar.bz2
Source1: slurm.init
Source2: slurmctld.init
Patch0: slurm-2.3.3-disable-bluegene.patch
URL: https://www.llnl.gov/linux/slurm
BuildRequires: openssl-devel
BuildRequires: gcc-c++
BuildRequires: pkgconfig(gtk+-2.0)
BuildRequires: python
BuildRequires: mysql-devel
BuildRequires: postgresql-devel
BuildRequires: munge-devel
BuildRequires: lua-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper

%define slurm_sysconfdir %{_sysconfdir}/slurm

%package -n %{libslurm}
Summary: Libraries for slurm
Group: System/Libraries

%package slurmctld
Summary: The main control daemon
Group: System/Cluster
Requires(post): rpm-helper
Requires(preun): rpm-helper

%package slurmdbd
Summary: Provides accounting of jobs in a database
Group: System/Cluster
Requires(post): rpm-helper
Requires(preun): rpm-helper

%package devel
Summary: Development package for SLURM
Group: Development/C
Requires: slurm
Requires: %{libslurm} = %EVRD

%package auth-none
Summary: SLURM auth NULL implementation (no authentication)
Group: System/Cluster
Requires: slurm

%package sched-wiki
Summary: SLURM scheduling plugin for the Maui scheduler
Group: System/Cluster
Requires: slurm

%package sview
Summary: SLURM graphical interface
Group: System/Cluster

%package db-pgsql
Summary: SLURM plugins to use PostgreSQL
Group: System/Cluster

%package db-mysql
Summary: SLURM plugins to use MySQL
Group: System/Cluster

%package auth-munge
Summary: SLURM plugins to use munge authentication
Group: System/Cluster

%description 
SLURM is an open source, fault-tolerant, and highly
scalable cluster management and job scheduling system for Linux clusters
containing up to thousands of nodes. Components include machine status,
partition management, job management, and scheduling modules.

%description -n %{libslurm}
This package contains the library needed to run programs dynamically linked
with slurm.

%description slurmctld
The main control daemon.

%description slurmdbd
Provides accounting of jobs in a database.

%description devel
Development package for SLURM.  This package includes the header files
and static libraries for the SLURM API.

%description auth-none
SLURM NULL authentication module

%description sched-wiki
SLURM scheduling plugin for the Maui scheduler.

%description sview
sview is a graphical user interface go get and update state information for
jobs, partitions, and nodes managed by SLURM.
# (taken from the quickstart)

%description db-pgsql
SLURM plugins to use a PostgreSQL database for job accounting.

%description db-mysql
SLURM plugins to use a MySQL database for job accounting.

%description auth-munge
SLURM plugins to use munge authentication.

%prep
%setup -q
%patch0 -p1 -b .disable-bluegene
chmod 0644 doc/html/*.{gif,jpg}

# blcr triggers a bug in automake
rm -f src/plugins/checkpoint/blcr/Makefile.am

%build
autoreconf -fiv
%configure --program-prefix=%{?_program_prefix:%{_program_prefix}} \
    --sysconfdir=%{slurm_sysconfdir}		\
    %{?_enable_debug}			\
    %{?with_proctrack}			\
    %{?with_ssl}			\
    %{?with_cflags}

%make

%install
rm -rf "%{buildroot}"
mkdir -p "%{buildroot}"
%makeinstall

install -D -m755 %{SOURCE1} %{buildroot}/%{_initrddir}/slurm
install -D -m755 %{SOURCE2} %{buildroot}/%{_initrddir}/slurmctld
install -D -m755 etc/init.d.slurmdbd %{buildroot}/%{_initrddir}/slurmdbd
install -D -m644 etc/slurm.conf.example ${RPM_BUILD_ROOT}%{slurm_sysconfdir}/slurm.conf.example
install -D -m755 etc/slurm.epilog.clean ${RPM_BUILD_ROOT}%{slurm_sysconfdir}/slurm.epilog.clean

# Delete unpackaged files:
rm -rf %{buildroot}/%{_libdir}/slurm/*.{a,la} \
	%{buildroot}/%{_libdir}/*.la \
	%{buildroot}/%{_datadir}/doc/slurm-%{version}/ \
	%{buildroot}/%{_mandir}/man5/bluegene*

%files
%doc AUTHORS
%doc NEWS
%doc README.rst
%doc RELEASE_NOTES
%doc DISCLAIMER
%doc COPYING
%doc etc/slurm.conf.example
%doc etc/slurmdbd.conf.example
%doc etc/cgroup.conf.example
%doc etc/cgroup.release_common.example
%doc etc/cgroup_allowed_devices_file.conf.example
%doc doc/html
%{_bindir}/sacct
%{_bindir}/sacctmgr
%{_bindir}/salloc
%{_bindir}/sattach
%{_bindir}/sbatch
%{_bindir}/sbcast
%{_bindir}/scancel
%{_bindir}/scontrol
%{_bindir}/sinfo
%{_bindir}/sprio
%{_bindir}/squeue
%{_bindir}/sreport
%{_bindir}/srun
%{_bindir}/smap
%{_bindir}/sshare
%{_bindir}/sdiag
%{_bindir}/sstat
%{_bindir}/strigger
%{_initrddir}/slurm
%{_sbindir}/slurmd
%{_sbindir}/slurmstepd
%{_libdir}/slurm/src/*
%{_mandir}/man1/sacct.1*
%{_mandir}/man1/sacctmgr.1*
%{_mandir}/man1/salloc.1*
%{_mandir}/man1/sattach.1*
%{_mandir}/man1/sbatch.1*
%{_mandir}/man1/sbcast.1*
%{_mandir}/man1/scancel.1*
%{_mandir}/man1/scontrol.1*
%{_mandir}/man1/sinfo.1*
%{_mandir}/man1/slurm.1*
%{_mandir}/man1/smap.1*
%{_mandir}/man1/sprio.1*
%{_mandir}/man1/squeue.1*
%{_mandir}/man1/sreport.1*
%{_mandir}/man1/srun.1*
%{_mandir}/man1/srun_cr.1*
%{_mandir}/man1/sshare.1*
%{_mandir}/man1/sstat.1*
%{_mandir}/man1/strigger.1*
%{_mandir}/man1/sdiag.1*
%{_mandir}/man5/slurm.conf.5.*
%{_mandir}/man5/cgroup.conf.5*
%{_mandir}/man5/cray.conf.5*
%{_mandir}/man5/gres.conf.5*
%{_mandir}/man5/topology.conf.5*
%{_mandir}/man8/slurmd.8.*
%{_mandir}/man8/slurmstepd.8.*
%{_mandir}/man8/spank.8.*
%dir %{_libdir}/slurm
%{_libdir}/slurm/checkpoint_none.so
%{_libdir}/slurm/jobacct_gather_cgroup.so
%{_libdir}/slurm/mpi_pmi2.so
%{_libdir}/slurm/job_submit_lua.so
%{_libdir}/slurm/proctrack_lua.so
%{_libdir}/slurm/jobacct_gather_linux.so
%{_libdir}/slurm/jobacct_gather_none.so
%{_libdir}/slurm/jobacct_gather_aix.so
%{_libdir}/slurm/jobcomp_none.so
%{_libdir}/slurm/jobcomp_filetxt.so
%{_libdir}/slurm/jobcomp_script.so
%{_libdir}/slurm/proctrack_pgid.so
%{_libdir}/slurm/proctrack_linuxproc.so
%{_libdir}/slurm/sched_backfill.so
%{_libdir}/slurm/sched_builtin.so
%{_libdir}/slurm/sched_hold.so
%{_libdir}/slurm/select_cons_res.so
%{_libdir}/slurm/select_linear.so
%{_libdir}/slurm/switch_none.so
%{_libdir}/slurm/mpi_none.so
%{_libdir}/slurm/mpi_mpichgm.so
%{_libdir}/slurm/mpi_mvapich.so
%{_libdir}/slurm/mpi_lam.so
%{_libdir}/slurm/task_none.so
%{_libdir}/slurm/task_affinity.so
%{_libdir}/slurm/accounting_storage_filetxt.so
%{_libdir}/slurm/accounting_storage_none.so
%{_libdir}/slurm/checkpoint_ompi.so
%{_libdir}/slurm/crypto_openssl.so
%{_libdir}/slurm/gres_gpu.so
%{_libdir}/slurm/gres_nic.so
%{_libdir}/slurm/job_submit_cnode.so
%{_libdir}/slurm/job_submit_defaults.so
%{_libdir}/slurm/job_submit_logging.so
%{_libdir}/slurm/job_submit_partition.so
%{_libdir}/slurm/mpi_mpich1_p4.so
%{_libdir}/slurm/mpi_mpich1_shmem.so
%{_libdir}/slurm/mpi_mpichmx.so
%{_libdir}/slurm/mpi_openmpi.so
%{_libdir}/slurm/preempt_none.so
%{_libdir}/slurm/preempt_partition_prio.so
%{_libdir}/slurm/preempt_qos.so
%{_libdir}/slurm/priority_basic.so
%{_libdir}/slurm/priority_multifactor.so
%{_libdir}/slurm/proctrack_cgroup.so
%{_libdir}/slurm/select_cray.so
%{_libdir}/slurm/task_cgroup.so
%{_libdir}/slurm/topology_3d_torus.so
%{_libdir}/slurm/topology_node_rank.so
%{_libdir}/slurm/topology_none.so
%{_libdir}/slurm/topology_tree.so
%{_libdir}/slurm/auth_none.so
%dir %{_libdir}/slurm/src
%config %{slurm_sysconfdir}/slurm.conf.example
%config(noreplace) %{slurm_sysconfdir}/slurm.epilog.clean

%files -n %{libslurm}
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%dir %attr(0755,root,root) %{_prefix}/include/slurm
%{_prefix}/include/slurm/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_mandir}/man3/*

%files slurmctld
%{_initrddir}/slurmctld
%{_sbindir}/slurmctld
%{_mandir}/man8/slurmctld.8.*

%files slurmdbd
%{_sbindir}/slurmdbd
%{_initrddir}/slurmdbd
%{_libdir}/slurm/accounting_storage_slurmdbd.so
%{_mandir}/man8/slurmdbd.8.*
%{_mandir}/man5/slurmdbd.conf.5.*

%files sched-wiki
%{_libdir}/slurm/sched_wiki*.so
%{_mandir}/man5/wiki.*

%files sview
%{_bindir}/sview
%{_mandir}/man1/sview.1*

%files db-pgsql
%{_libdir}/slurm/accounting_storage_pgsql.so
%{_libdir}/slurm/jobcomp_pgsql.so

%files db-mysql
%{_libdir}/slurm/accounting_storage_mysql.so
%{_libdir}/slurm/jobcomp_mysql.so

%files auth-munge
%{_libdir}/slurm/auth_munge.so
%{_libdir}/slurm/crypto_munge.so

%pre
%_pre_useradd slurm / /sbin/nologin

%post
%_post_service slurm

%post slurmctld
%_post_service slurmctld

%post slurmdbd
%_post_service slurmdbd

%preun
%_preun_service slurm

%preun slurmctld
%_preun_service slurmctld

%preun slurmdbd
%_preun_service slurmdbd
