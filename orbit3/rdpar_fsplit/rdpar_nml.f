       SUBROUTINE rdpar_nml
C*********************************************************************
c
c    This subroutine reads all the parameters from the input file.
c  (This stuff used to be in the main program.)
c
C*********************************************************************

      include 'dcalc.h'
      save

      character*80 ifname 
      character*80 ifdir 
      character*80 limfnam
      character*80 limfdir

        
      common/efitcom/ifname,ifdir
      common/limnam/limfnam,limfdir
      common/magcom/icur,cur,bt,scale
      common/geocom/rmax,V0,W1,W2
      common/p14com/zdet,adet,ener 

      parameter(mxorpt=64000)
      
      common/data5/x(mxorpt+1),y(mxorpt+1),z(mxorpt+1),
     >    x2(mxorpt+1),y2(mxorpt+1)

      common/switch/ifor,ipl1,ipl2,irmn,rarray(201),rmn,ipoldir

      common/char/fname,coment
      common /versn/ codenm, compdt, comptm
      common/iter/iters(5),start(5),stop(5),step(5),name(5)
      dimension save(5)
      common /data6/ iflxplt, steppsi(mxorpt+1), pphi(mxorpt+1),
     .    mu(mxorpt+1), energy(mxorpt+1), b_r(mxorpt+1), b_phi(mxorpt+1), 
     .    b_z(mxorpt+1)
      real*8 mu
      common/shftcm/is

      logical eq99
      real*8 is
      character*6 ifil
      character*80 fname
      character*80 coment
      character*9  compdt, comptm
      character*35 codenm
      character*9 rundt, runtm

c
c     coment      comment field describing this run of code
c     codenm      name of this version of code
c     compdt      compilation date of code (manual for now, auto later?)
c     comptm      compilation time of code (")
c     rundt       date of current run of code
c     runtm       time of current run of code
c

      common /magsrc/ magfil
      character*60 magfil

c     MAGFIL	  name of file containing CHS coil currents

c                        The following common block is for 2 plots per page!

      common /plot2/ ixlpol2, ixhpol2, jybpol2, jytpol2, ixlpln2, ixhpln2,
     .   jybpln2, jytpln2

c  IXLPOL2, IXHPOL2      Low & high screen coords for poloidal view x-axis
c  JYBPOL2, JYTPOL2      Bottom & top screen coords for poloidal view y-axis
c  IXLPLN2, IXHPLN2      Low & high screen coords for plan view x-axis
c  JYBPLN2, JYTPLN2      Bottom & top screen coords for plan view y-axis

c                        The following common block is for 3 plots per page!

      common /plot3/ ixlpol3, ixhpol3, jybpol3, jytpol3, ixlelv3, ixhelv3, 
     .   jybelv3, jytelv3, ixlpln3, ixhpln3, jybpln3, jytpln3

c  IXLPOL3, IXHPOL3      Low & high screen coords for poloidal view x-axis
c  JYBPOL3, JYTPOL3      Bottom & top screen coords for poloidal view y-axis
c  IXLELV3, IXHELV3      Low & high screen coords for elevation view x-axis
c  JYBELV3, JYTELV3      Bottom & top screen coords for elevation view y-axis
c  IXLPLN3, IXHPLN3      Low & high screen coords for plan view x-axis
c  JYBPLN3, JYTPLN3      Bottom & top screen coords for plan view y-axis

c                        The following common block is for the real coords of
c                          the plot box sizes

      common /plotr/ xlpol, xhpol, ybpol, ytpol, xlelv, xhelv, ybelv, ytelv, 
     .   xlpln, xhpln, ybpln, ytpln
      real*4 xlpol, xhpol, ybpol, ytpol, xlelv, xhelv, ybelv, ytelv, 
     .   xlpln, xhpln, ybpln, ytpln

c  XLPOL,   XHPOL        Low & high real coords (m) for poloidal view x-axis
c  YBPOL,   YTPOL        Bottom & top real coords (m) for poloidal view y-axis
c  XLELV,   XHELV        Low & high real coords (m) for elevation view x-axis
c  YBELV,   YTELV        Bottom & top real coords (m) for elevation view y-axis
c  XLPLN,   XHPLN        Low & high real coords (m) for plan view x-axis
c  YBPLN,   YTPLN        Bottom & top real coords (m) for plan view y-axis

c                        Text position in orbit plot

      common /plttxt/ ixtxt, jytxt
      integer ixtxt, jytxt

c  IXTXT                 Screen x-coord for left side of parameter listing
c  JYTXT                 Screen y-coord for top of parameter listing

c                        Color codes for plot elements follow:

      common /pltclr/ icfr, icorb, iclim, icflx, ictxt

c  ICFR                  Code for color of axes of graphs (defaults to black?)
c  ICORB                 Code for color of orbit
c  ICLIM                 Code for color of limiter
c  ICFLX                 Code for color of flux contours
c  ICTXT                 Code for color of text info

      common /psix/ npsiplt, simin, simax
      integer npsiplt
      real*8 simin, simax

c  NPSIPLT    number of psi contours to plot in output
c  SIMIN      minimum value of psi (poloidal flux) on grid
c  SIMAX      maximum value of psi (poloidal flux) on grid

c parameters to describe profile
!      parameter( n_par = 10)
      real*8 par(n_par)

      common /em_par/model, par

      integer*4 dum
      integer iret

c     DUM         dummy variable to read comment lines in input file

c WB using namelist for input

      namelist /general/ COMENT, ifname, ifdir, limfnam, limfdir, 
     >     efflim, bfield_scale, detectors, iteration

      namelist /orbit_par/
     > detectors, detector_number, theta_port, phi_port, gyro_angle, 
     > pitch_angle, part_energy, channel_number, detector_id

c	  RD is major radius of detector, in cm.
c	  ZD is Z-position of detector, in cm.
c	  PHD is toroidal angle of detector, in radians.
c	  ZDET is charge of particle (in electron charges)
c	  ADET is mass of particle (in proton masses)
c	  ENER is energy of particle in MeV
c	  S is single step size, in m.
c	  SSTP is maximum orbit length, in m.
c	  TOL is orbit integrator tolerance param, (1e-5)
c	  D is spacing between collimating aperture
c	  and detector aperture, in cm.
c	  RC is collimator radius
c	  XC is half-width of colimator, in cm.
c	  YC is half-height of collimator, in cm
c	  XD is half-width of detector aper, in cm
c	  YD is half-height of detector aper, in cm
c	  NX & NY subdivide the aperture in pieces

      namelist /detection/
     > RDist, ZDist, phdangle, ZDET,ADET,
     > S, SSTP, tol, D, RC, RCD,
     > XC, YC, XD, YD, NX, NY, NSEG

c	  IFOR is 0 for time-reversed orbit, 1 o.w.
c	  IPL1 is 0 for no orbit plot, 1,2,3=# plots
c	  IRMN is 1 to plot minimum minor radius of 
c	  each orbit, 0 o.w.
c	  V0 is major radius of vessel center
c	  RMAX has something to do with DIII-D vacuum
c     vessel shape (not used in other versions)
c     IPOLDIR 1 switch the direction of the poloidal field
c             0 keep is as in the file

      namelist /control/
     > IFOR, IPL1, IRMN, iflxplt,
     > v0, rmax, npsiplt, ipoldir
c
c model: model for emissivity 1: power law : psi**par(1)
c                             2: gauss: par(1)*exp( - ( (psi-par(2))/par(3))**2)
c                             3: hollow gauss: g1 - g2 g2: par(4)*exp( - ( (psi-par(2))/par(5))**2)
      namelist /emissivity/
     > model, par



c***************************begin executable code *******************
c     initialize some values
c do not change direction of poloidal field      
      ipoldir = 0 

c convert degrees to radians
      dtr = 0.017453292519943295

c FNAME is the parameter file name
      print *,  'rdpar: using parameter file: ', FNAME 

      OPEN(UNIT=23,FILE=FNAME,STATUS='old')      

c read parameters
      
c general parameters
      read(23, nml=general)
      write(*, nml=general)

c control parameters
      read(23, nml = control)
      write(*, nml = control)

c control parameters
      read(23, nml = emissivity)
      write(*, nml = emissivity)

c orbit generation parameters
      read(23, nml = orbit_par)
      write(*, nml = orbit_par)

	      if (detectors .gt. n_par) then
		write(*,*) 'Too many detectors; maximum allowed ', n_par
		stop
      end if
 
      detec = detectors

c detection parameters
      read(23, nml = detection)
      write(*, nml = detection)

      rewind(23)

c magnetic field scaling mostly for testing
      scale = bfield_scale

c settinng up the port variables

		do i = 1, detec
          ports(i) = theta_port(detector_number(i))*dtr

			portsph(i) = phi_port(detector_number(i))*dtr

			Al0s(i) = gyro_angle(detector_number(i))*dtr

			be0s(i) = pitch_angle(detector_number(i))*dtr

			rds(i) = rdist(detector_number(i))

			zds(i) = zdist(detector_number(i))

			phda(i) = phdangle(detector_number(i))*dtr
            
          rcol(i) = rc(detector_number(i))
          
          rcdet(i) = rcd(detector_number(i))
		end do

!      if (vary_theta_port) then
!       iters(1) = 1
 !        stop(1) = theta_port_stop*dtr
  !       step(1) = theta_port_step*dtr
!      endif
 !     portph = phi_port*dtr

!	if (vary_phi_port) then

!	    iters(6) = 1.

!	end if

c setup gyro angle
 !     AL0 = gyro_angle*dtr
      
!	if (vary_gyro_angle) then
!		iters(3) = 1
!	end if

!	do i = 1, iteration
!		if (vary_gyro_angle) then
 !        		Al0s(i) = gyro_angle(i)*dtr
 !     		else
!			al0s(i) = gyro_angle(1)*dtr
 !        stop(3) = gyro_angle_stop*dtr 
 !        step(3) = gyro_angle_step*dtr
  !    		endif
!	end do

c setting up pitch angle
!      BE0 = pitch_angle*dtr
!      if (vary_pitch_angle) then
!         iters(2) = 1
 !        stop(2) = pitch_angle_stop*dtr
 !        step(2) = pitch_angle_step*dtr
!      endif

!	if (vary_pitch_angle) then
!		iters(2) = 1
!	end if

!	do i = 1, iteration
!		if (vary_pitch_angle) then
 !        		be0s(i) = pitch_angle(i)*dtr
  !    		else
!			be0s(i) = pitch_angle(1)*dtr
 !        stop(3) = gyro_angle_stop*dtr 
 !        step(3) = gyro_angle_step*dtr
 !     		endif
!	end do

c setting up particle energy
      ENER = part_energy
!      if (vary_pitch_angle) then
!         iters(5) = 1
!         stop(5) = part_energy_stop
!         step(5) = part_energy_step
!      endif


      if (d .le. 0) then
        write (6, *) ' ** Spacing between detector & collimator is <0: '
     .    , d
        close(23)
        stop
      endif

      if ((xc+xd .eq. 0.0) .or. (yc+yd .eq. 0.0)) then
        write (6,*) ' ** Detector & collimator dimensions in X or Y ',
     .     'sum to zero!'
        close (23)
      endif

      CLOSE(UNIT=23)
      return

c	  execute below if file open error

c 1001  CALL ERRSNS(I,J)
1001  PRINT 1011,IRET
1011  FORMAT(' PARAMETER INPUT FILE OPEN ERROR:',I6,2X/
     1  ' SEE COGNIZANT PROGRAMMER.')
      call finitt (0, 0)

      stop


      end


