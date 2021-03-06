# Halo.py
# Description: Container class for storing halo information
#
# Class: CS 594 - Spring 2015
# System: Windows 8.1, Python 2.7.8 (Anaconda 2.1.0 - x64), VTK 6.1.0 (x64)
# Author: Arthur Nishimoto (anishi2)

import numpy as np

class Halo:
    def __init__(self, data):
		self.data = "hello";
		self.scale = data[0] #Scale: Scale factor of halo.
		self.id = int(data[1]) #ID: ID of halo (unique across entire simulation).
		self.desc_scale = data[2] #Desc_Scale: Scale of descendant halo, if applicable.
		self.desc_id = int(data[3]) #Descid: ID of descendant halo, if applicable.
		self.num_prog = int(data[4]) #Num_prog: Number of progenitors.
		self.pid = int(data[5]) #Pid: Host halo ID (-1 if distinct halo).
		self.upid = int(data[6]) #Upid: Most massive host halo ID (only different from Pid in cases of sub-subs, or sub-sub-subs, etc.).
		self.desc_pid = data[7] #Desc_pid: Pid of descendant halo (if applicable).
		self.phantom = data[8] #Phantom: Nonzero for halos interpolated across timesteps.
		self.sam_mvir = data[9] #SAM_Mvir: Halo mass, smoothed across accretion history; always greater than sum of halo masses of contributing progenitors (Msun/h).  Only for use with select semi-analytic models.
		self.mvir = data[10] #Mvir: Halo mass (Msun/h).
		self.rvir = data[11] #Rvir: Halo radius (kpc/h comoving).
		self.rs = data[12] #Rs: Scale radius (kpc/h comoving).
		self.vrms = data[13] #Vrms: Velocity dispersion (km/s physical).
		self.mmp = data[14] #mmp?: whether the halo is the most massive progenitor or not.
		self.scale_of_last_MM = data[15] #scale_of_last_MM: scale factor of the last major merger (Mass ratio > 0.3).
		self.vmax = data[16] #Vmax: Maxmimum circular velocity (km/s physical).
		self.position = [float(data[17]), float(data[18]), float(data[19])] #X/Y/Z: Halo position (Mpc/h comoving).
		self.velocity = [float(data[20]), float(data[21]), float(data[22])] #VX/VY/VZ: Halo velocity (km/s physical).
		self.angVel = [float(data[23]), float(data[24]), float(data[25])] #JX/JY/JZ: Halo angular momenta ((Msun/h) * (Mpc/h) * km/s (physical)).
		self.Spin = data[26] #Spin: Halo spin parameter.
		self.Breadth_first_ID = data[27] #Breadth_first_ID: breadth-first ordering of halos within a tree.
		self.Depth_first_ID = data[28] #Depth_first_ID: depth-first ordering of halos within a tree.
		self.Tree_root_ID = data[29] #Tree_root_ID: ID of the halo at the last timestep in the tree.
		self.Orig_halo_ID = data[30] #Orig_halo_ID: Original halo ID from halo finder.
		self.Snap_num = data[31] #Snap_num: Snapshot number from which halo originated.
		self.Next_coprogenitor_depthfirst_ID = data[32] #Next_coprogenitor_depthfirst_ID: Depthfirst ID of next coprogenitor.
		self.Last_progenitor_depthfirst_ID = data[33] #Last_progenitor_depthfirst_ID: Depthfirst ID of last progenitor.
		self.Rs_Klypin = data[34] #Rs_Klypin: Scale radius determined using Vmax and Mvir (see Rockstar paper)
		self.M_all = data[35] #M_all: Mass enclosed within the specified overdensity, including unbound particles (Msun/h)
		self.M200b = data[36] #M200b--M2500c: Mass enclosed within specified overdensities (Msun/h)
		self.M200c = data[37] 
		self.M500c = data[38] 
		self.M2500c = data[39] 
		self.Xoff = data[40] #Xoff: Offset of density peak from average particle position (kpc/h comoving)
		self.Voff = data[41] #Voff: Offset of density peak from average particle velocity (km/s physical)
		self.Spin_Bullock = data[42] #Spin_Bullock: Bullock spin parameter (J/(sqrt(2)*GMVR))
		self.b_to_a = data[43] #b_to_a, c_to_a: Ratio of second and third largest shape ellipsoid axes (B and C) to largest shape ellipsoid axis (A) (dimensionless).
		self.c_to_a = data[44] #  Shapes are determined by the method in Allgood et al. (2006). #  (500c) indicates that only particles within R500c are considered.
		self.a = [data[45], data[46], data[47]] #A[x],A[y],A[z]: Largest shape ellipsoid axis (kpc/h
		self.b_to_a500c = data[48] 
		self.c_to_a500c = data[49]
		self.a500c = [data[50], data[51] , data[52]]
		self.kinToPotRatio = data[53] #T/|U|: ratio of kinetic to potential energies
		self.M_pe_Behroozi = data[54] 
		self.M_pe_Diemer = data[55] 
		self.Macc = data[56] 
		self.Mpeak = data[57] 
		self.Vacc = data[58] 
		self.Vpeak = data[59] 
		self.Halfmass_Scale = data[60] 		
		self.Acc_Rate_Inst = data[61] 		
		self.Acc_Rate_100Myr = data[62] 		
		self.Acc_Rate_Tdyn = data[63]
		
		self.clients = {}
		self.positions = []
		self.rootHaloID = -1
		
		self.nextDesc_id = -1

		self.trackedPos = np.empty(0)
		self.trackedVel = np.empty(0)