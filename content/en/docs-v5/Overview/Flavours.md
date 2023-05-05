---
title: Flavours
weight: 2
---

Photon OS consists of a minimal version, a full version, RPM OSTree, and Photon Real-Time Operating System.


- The minimal version of Photon OS is lightweight container host runtime environment that is suited to managing and hosting containers. The minimal version contains just enough packaging and functionality to manage and modify containers while remaining a fast runtime environment. The minimal version is ready to work with appliances. 


- The Developer version of Photon OS includes additional packages to help you customize the system and create containerized applications. For running containers, the developer version is excessive. The developer version helps you create, develop, test, and package an application that runs a container. 

- OSTree is a tool to manage bootable, immutable, versioned filesystem trees. Unlike traditional package managers like rpm or dpkg that know how to install, uninstall, configure packages, OSTree has no knowledge of the relationship between files. But when you add rpm capabilities on top of OSTree, it becomes RPM-OSTree, meaning a filetree replication system that is also package-aware.

- Photon OS features a kernel flavor called `linux-rt` to support low-latency real time applications. linux-rt is based on the Linux kernel PREEMPT_RT patchset that turns Linux into a hard real time operating system. In addition to the real time kernel itself, Photon OS 5.0 supports several userspace packages such as tuned, tuna, stalld, and others, that are useful to configure the operating system for real time workloads. The linux-rt kernel and the associated userspace packages together are referred to as Photon Real Time (RT).      
In Photon OS 5.0, the `linux-rt` kernel flavor comes with the following improvements:

	- **Low-latency Optimizations**: Low-latency is achieved with the following feature enhancements:

		-  Guest Timer Advancement feature in `linux-rt` mitigates the cost of timer virtualization on ESXi. This makes Photon RT on ESXi and bare-metal indistinguishable in terms of the cyclictest benchmark results.
		-  Enhancements to tuned and trace-cmd packages to reduce OS jitter to real-time workloads.

	- **Stability Enhancements**: Enhanced stability is achieved with the following improvements:
		
		- `stalld` version is updated to 1.17.1, which brings in several improvements to the effectiveness and efficiency of `stalld` in resolving kernel thread starvation.
		- Updated `stalld` configuration file with more effective and field-proven defaults.

	- **Debugging Enhancements:**: Debugging enhancements are achieved with the following improvements:

		- To aid with latency tuning and debugging, osnoise and timerlat latency tracers are enabled in the `linux-rt` kernel.
		- Enabled Kernel's hung-task detector in tuned real-time profile's configuration.

	- **Hardware Enablement**: Support is added for Intel Sapphire Rapids CPUs, including its Telco-specific 5G ISA.

	- **Driver Updates**: Updated out-of-tree Intel network drivers to the following versions:
		- i40e – v2.22.18
		- iavf – v4.8.2
		- ice – v1.11.14



