      SUBROUTINE CHRIEN(jdet)
C*********************************************************************
C*********************************************************************
C   W.HEIDBRINK      3/82
C   H.DUONG          4/89
C   THIS ROUTINE CALCULATES DETECTOR EFFICIENCY USING THE FORMULA IN
C   BOB CHRIEN'S THESIS DIVIDED BY  4PI.
C   IT USES THAL4 AND MAGFLD TO FOLLOW ORBITS.
C   THE DETECTOR-APERTURE SYSTEM IS ASSUMED TO BE SLOT-
C   TED.  THE DETECTOR IS ASSUMED TO HAVE ITS NORMAL
C   PARALLEL TO THE Z AXIS WHEN PORT=0.
C   AL0 AND BE0 REPRESENT VARIATIONS ABOUT THIS NORMAL.
C   THE INPUT PARAMETER PORT DETERMINES THE 
C   ORIENTATION OF THE DETECTOR NORMAL.
C   THE ANGULAR WEIGHTING IS CORRECT (TRIANGULAR) FOR SLOTS.
C   NX AND NY DETERMINE HOW MANY ORBITS ARE CALCULATED.
C   NX AND NY SHOULD BE ODD INTEGERS.
C   IF NX=NY=1 ONLY ONE ORBIT IS CALCULATED.
C   ALTHOUGH A CONVENTIONAL CYLINDRICAL COORDINATE SYSTEM IS USED
C   BY THAL4, IN ORDER TO TIME-REVERSE THE ORBITS NOT ONLY THE
C   SIGN OF THE VELOCITY MUST BE REVERSED, BUT ALSO THE SIGN OF THE
C   MAGNETIC FIELD (IF THE FORCE LAW IS PRESERVED UNCHANGED).
C   THE POSITIVE DIRECTION FOR BT AND CUR IS THEREFORE CLOCKWISE
C   AS VIEWED FROM ABOVE.
C   THE DOMEGA LOOP HAS BEEN CORRECTED FOR CASES WHEN 
C   AL0 AND/OR BE0 ARE .NE. TO ZERO, IE. SLANTED COLLIMATORS.
C
C  WB changed the acceptance calculation, by adding the routine accept
C     changes the binning of the acceptance

C JDET: detector index that is currently being worked on
C********************************************************************
C********************************************************************
      
      include 'dcalc.h'
      include 'eparmdu129.h'      

      save
      
      integer jdet 

      integer plotmed2

      COMMON/MW1COM/MW1,MH1
      COMMON/GTABLE/RGRID(NW),ZGRID(NH)
      COMMON/CONSTS/PM,ECHRG,EMASS,PI
      COMMON/MAGCOM/ICUR,CUR,BT
      COMMON/GEOCOM/RMAX,V0
      COMMON/P14COM/ZDET,ADET,ENER

      common /ixiy/ ix, iy
      integer ix, iy


      common /iounit/iorbit, icounter, orbit_fname
      character *80 orbit_fname

      
      parameter (mxorpt=64000)
c orbit position data
      common/data5/x(mxorpt+1),y(mxorpt+1),z(mxorpt+1),
     .     x2(mxorpt+1),y2(mxorpt+1), b_r(mxorpt+1), b_phi(mxorpt+1), 
     .    b_z(mxorpt+1)
c orbit flux data etc.      
      common /data6/ iflxplt, steppsi(mxorpt+1), pphi(mxorpt+1),
     .     mu(mxorpt+1), energy(mxorpt+1), vpar(mxorpt+1), vperp(mxorpt+1),
     .     bmod(mxorpt+1), rho(mxorpt+1), lborho(mxorpt+1)

      common /sdl_data/sdl_cs(mxorpt+1)

      real*8 mu, lborho
      
c     IFLXPLT    1 if particle flux surface vs step is to be plotted, 0 o.w.
c     STEPSPI    poloidal flux at particle position as a function of time
c     PPHI       canonical toroidal momentum of particle as function of time
c     MU         magnetic moment of particle as function of time
c     ENERGY     energy of particle as function of time
c     VPAR       parallel velocity of particle as function of time
c     VPERP      perpendicular velocity of particle as function of time
c     BMOD       magnitude of B at particle location as function of time
c     RHO        particle gyroradius as function of time
c     LBORHO     magnetic field scale length over particle gyroradius as fcn of t
c     SDL_SC     cumulative sum of sdl
c     /CFFOL/ contains info from EFIT magnetics
      
      common/cffol/qpsi(nw),bfpol(nw),cfpol(nw),dfpol(nw),mwfpol,
     .     rbdry(mbdry),zbdry(mbdry),nbdry,xxxsi(nw),sifm,sifb
     .     ,rzero,bzero,piii,qout95,pcurrt(nwnh)
      
      integer nyflat, nxflat, nyflat_save, nxflat_save, ijstart,
     .     ijend, iistart, iiend
      real*8 tr_fact_nx(201), tr_fact_ny(201)
      
c     TR_FACT_NX	transmission factor for each step in NX iteration
c     TR_FACT_NY	transmission factor for each step in NY iteration
c     NXFLAT	value in NX iteration at which X-transmission is 1.0
c     NYFLAT	value in NY iteration at which Y-transmission is 1.0
      
      common /ptch/ riptch
      
c     RIPTCH	the real initial pitch angle relative to the magnetic field
      
      common /psix/ npsiplt, simin, simax
      integer npsiplt
      real*8 simin, simax
      
c     NPSIPLT    number of psi contours to plot in output
c     SIMIN      minimum value of psi (poloidal flux) on grid
c     SIMAX      maximum value of psi (poloidal flux) on grid
      

      common/switch/ifor,ipl1,ipl2,irmn,rarray(201),rmn,ipoldir

      DIMENSION ORD(115),ORD2(115),ABSC(115)
      DIMENSION RINIT(4), RT(3), RT0(3), RT_INIT(3), RT_BR(3)

c string to create outout data file names
      character orbit_dir*30
      character orbit_head*30
      character orbit_tail*30
      character orbit_id*7

      real*8 psirel
      DATA C/3.0d8/

      data orbit_dir/'./orb/'/
      data orbit_head/'track_'/
      data orbit_tail/'.data'/
      
c     Note: Formula inserted for JET version to modify neutron source
c     profile to be proportional to psirel**is where psirel is zero at
c     the plasma edge and 1 at the axis, and is just a linear function
c     of the poloidal flux.
      
C......CALCULATE SDV
      
c~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c     the rdameqk subroutine reads in information from a file but the file
c     is missing which is why the error statement originally came up, 
c     therefore there is no reason to call this subroutine as it cannot
c     read the file and simply produces an error
c~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	write(*,*) 'Portph =', portph


c     call rdameqk(RCHK,ZCHK,ACHK,ECHK)
      
c     sdv= 0.0
      
c     ACHK2=ACHK**2.0
c     this is not needed because the if statement involving it was commented
      
d     write (8,*) ' Before SdV calculation, achk=', achk
d     write (8,*) ' sifb=', sifb,' sifm=',sifm

      icounter = icounter + 1
      sdv=0
c     write flux to data file
c     calculate total yield
      print *, 'Prepare flux.data, existing parameters :'
      print *, 'sifm (flux on axis), sifb (flux on bdry) = ', sifm,sifb
      
      open ( 50, file = 'flux.data')
      write (50,*) 
     >      '#! i[i,0]/ j[i,0]/ r[f,2]/ z[f,3]/'//
     >     ' psi[f,4]/ psirel[f,5]/ Em[f,6]/ '
      DO I=1,MW1 
         DO J=1,MH1
c   width, height position in R,Z plane width = R, height = Z            
            WIDTH=RGRID(I)
            HEIGHT=ZGRID(J)
            if (plotmed2 (psi, width, height) .eq. 1) then
               psirel = get_psirel(psi)
            else
               psirel = 0.
            endif
c     psi rgetel has a different sign than psi as at the center of the 
c     plasma psi is 0. 
c     sifb: flux value on the last closed flux surface (boundary)
c     sifm: minimum flux
            if (psirel. gt. 0) then
               Em_val = Em(psirel, width, height)
            else
               Em_val = 0.
            endif
            write (50,*) i, j, width, height, psi, psirel, Em_val
d     write (8,*) ' i, j=', i, j, ' psi=', psi, 'psirel=',psirel
            
            IF (psirel .LE. 0.0) cycle
c     
c     here we would add a new, more general emissivity
c     
c WB modified Em call to Em (psirel, R, Z)L
            SDV=SDV+RGRID(I)*Em_val
            
         END DO
      END DO 
      close(50)

c***************************************************************************
c Create data file for collimator radius and length.


      open ( 60, file = 'collimator.data')
      write (60,*) 
     >      '#! rc[f,0]/ d[f,1]/ '
      write (60,*) rc, d

      close(60)
      
      SDV=(SDV*2.0d0*PI*(RGRID(MW1)-RGRID(1)) 
     .     *(ZGRID(MH1)-ZGRID(1)))/(MW1*MH1)  
      
d     write (8,*) ' Final SdV=', sdv
      
c     total production rate 
      total_rate_sr = (SDV * 4.0d0 * PI)
      
C......SET PARTICLE INITIAL POSITION
c     
c     AL0 and BE0 are used to describe the offset of the
c     detector center with respect to the coll. center
c     
c     this can be used for slanted detector-collimator systems
c     this is the location of the center of the collimator
      
      RINIT(1)=RD
      RINIT(2)=phd
      RINIT(3)=ZD

c     detector position in cart. coord      
      rt0(1) = RD*cos(phd)
      rt0(2) = RD*sin(phd)
      rt0(3) = ZD

c      print *, 'RD, phd, ZD =', RD, phd, ZD
      
      XAL=D*SIN(AL0)/COS(AL0)
      
c     handle limiting angle case
      if (abs(be0) .ge. 1.570795) then
         ybe = sign(1.0d6, be0)
      else
         YBE=D*SIN(BE0)/COS(BE0)
      endif
      
      SUM=0.
      
C......ENTER DOMEGA LOOP.
D     write (8,*) ' xal= ', xal, ' ybe= ', ybe, ' alold= ', alold
      
      cp = cos(port)
      sp = sin(port)
      cpph = cos(portph)
      spph = sin(portph)
      
D     write (8,*) ' cp=', cp, ' sp=', sp, ' cpph=', cpph, ' spph=',spph
c     WB bin the entrance only

c     calculate the bin widths of the opening
      XC_bin = XC/real(NX)
      YC_bin = YC/real(NY)

c     do the same with the detector for the moment use the same binning as the collimator
      XD_bin = XD/real(NX)
      YD_bin = YD/real(NY)
      
      
c     start of the bin centers
      offset_x = real(NX+1)/real(NX)
      offset_y = real(NY+1)/real(NY)

      print *, 'XC, YC = ', XC, YC
      print *, 'XC_bin, YC_bin = ',  XC_bin, YC_bin
      print *, 'XD, YD = ', XD, YD
      print *, 'XD_bin, YD_bin = ',  XD_bin, YD_bin
      
      
      DO I=1,NSEG
         IF(I .EQ. 1) then
            XS = 0.
            YS = 0.
         ELSE
            XS = rcol(jdet)/2*(1+1/SQRT(real(NSEG)))*COS(2.*PI*(I-1)/(NSEG-1))
            YS = rcol(jdet)/2*(1+1/SQRT(real(NSEG)))*SIN(2.*PI*(I-1)/(NSEG-1))
         end if
         print *, 'xs, ys =', xs, ys
         DO ID = 1,NSEG
            print *, 'iteration = ', i, id
            IF(ID .EQ. 1) then
                XSD = 0.
                YSD = 0.
            ELSE
                XSD = rcdet(jdet)/2*(1+1/SQRT(real(NSEG)))*COS(2.*PI*(ID-1)/(NSEG-1))
                YSD = rcdet(jdet)/2*(1+1/SQRT(real(NSEG)))*SIN(2.*PI*(ID-1)/(NSEG-1))
            end if
            print *, 'xsd, ysd =', xsd, ysd
            XTOT = XS - XSD
            YTOT = YS - YSD
            GYRO=0.
            PITCH=0.
c      DO I=1,NX
c         ix = i
c         XS = (REAL(2*I)/NX - offset_x)*XC
cc     determine the direction of the line connecting the 
cc     center of the coll. bin and the center of the detector
c         do id = 1, NX
c            ixd = id
c            XSD = (REAL(2*ixd)/NX - offset_x)*XD
c            XTOT=XAL + XSD + XS
c            ALPH=ATAN(XTOT/D)
cD           write (8,*) ' xs= ', xs, ' xtot= ', xtot, ' alph= ', alph,
cD     .                 ' dalph= ', dalph, ' beold= ', beold
c
cc     WB bin entrance and detector in y-direction
c            DO J=1,NY
c               iy = j
c               YS = (REAL(2*J)/NY - offset_y)*YC
c               DO jd = 1,NY
c                  jyd = jd
c                  YSD = (REAL(2*jyd)/NY - offset_y)*YD
cc                 determine the direction of the line connecting the 
cc                 center of the coll. bin and the center of the detector        
c                  YTOT=YBE + YS + YSD
c                  BETA=ATAN(YTOT/D)
cc                 store the particle direction in the detector system
cc                   GYRO=ALPH
cc                  PITCH=BETA
c                  GYRO=0.
c                  PITCH=0.
c                  print *, XAL, XS, XSD, XTOT, YBE, YS, YSD, YTOT
cD                 write (8,*) ' ys= ', ys, '0 ytot= ', ytot, ' beta= ',
cD     .                       beta, ' dbeta= ', dbeta, ' gyro= ', gyro, ' pitch= ', pitch
c            
C.................INITIALIZE POSITION.
c                 to be precise one should convert the xs/ys into toroidal coord to take the shift in the collimator
c                 into account which is at the moment ignored
                  zs = 0.
c                  zs = -D
                
c                 transformation from detector coordinate system to NSTX coordinate system and add to detector center position
c                 added rotation around z by phd angle                  
                  rt_br(1) = xs*cp - ys*sp*spph - zs*sp*cpph
                  rt_br(2) = ys*cpph - zs*spph
                  rt_br(3) = xs*sp + ys*cp*spph + zs*cp*cpph
                  
c                  rt(1) = rt_br(1)
c                  rt(2) = rt_br(2)
c                  rt(3) = rt_br(3)
                  
                  rt(1) = rt_br(1)*cos(phd) - rt_br(2)*sin(phd) + rt0(1)
                  rt(2) = rt_br(1)*sin(phd) + rt_br(2)*cos(phd) + rt0(2) 
                  rt(3) = rt_br(3) + rt0(3)
c     convert to toroidal coords (works only if phd is within +/- pi/2.)
                  rt_init(1) = sqrt(rt(1)**2 + rt(2)**2)
                  IF (rt(2) .GE. 0.) rt_init(2) = acos(rt(1)/rt_init(1))
                  IF (rt(2) .LT. 0.) rt_init(2) = 2*PI - acos(rt(1)/rt_init(1))
                  rt_init(3) = rt(3)
                
                  DO K=1,3
c                     R(K)=RINIT(K)
                     R(K)=RT_INIT(K)
                  enddo
		
            
C.................CALCULATE INITIAL VELOCITIES (TIME-REVERSED).
c                 setup the velocity vector in int the detector coord. system
                  V(4)=1.
                  DIST=SQRT(D**2 + XTOT**2 + YTOT**2)
                  vx=XTOT/DIST
                  vy=YTOT/DIST
                  vz=SQRT(1. - vx**2 - vy**2)
D                 write (8,*) ' vx, vy, vz=', vx, vy, vz
            
c                 transformation from detector coordinate system to NSTX coordinate system
                  v(1) = vx*cp - vy*sp*spph - vz*sp*cpph
                  v(2) = vy*cpph - vz*spph
                  v(3) = vx*sp + vy*cp*spph + vz*cp*cpph
            
                  print *, 'detector v: ', vx, vy, vz
                  print *, 'NSTX     v: ', v(1), v(2), v(3)
C.................FIND ORBIT AND STORE IT IN X,Y,Z
            
D                 write (8,*) ' v= ', v
            
c                 maximal number of step to evaluate
                  N=SSTP/S
                  IF(N .GT. mxorpt) N=mxorpt
d                 print*,'ready to call thal4 in subroutine chrien'
            
c                 N: number of real steps is returned from THAL4 
                  CALL THAL4(N)
            
c                 no step could be calculated for this orbit
                  IF(N.EQ.0) cycle
            
C.................CALCULATE SDL FOR THIS ORBIT
C.................and accumulate flux at each position for later plotting
            
                  SDL=0.0d0
c                 store the number of steps in the first element of the array steppsi
                  steppsi(1) = n
D                 write (8,*) 'Starting SdL calculation'
c                 loop over the steps
                  DO L=1,N
c                    calculate psirel for current step, note that the psi data start
c                    at index 2
                     psirel = get_psirel(steppsi(l+1))
D                    write (8,*) ' orbit step: ',l,' X,Z=',x(l+1),z(l+1),
D     >                          ' flux=',steppsi(l+1),' psirel=',psirel
               
c                    psirel >=0. we are inside the plasma            
                     IF (psirel .gt. 0.0d0) then
                        r_step = x(l+1)
                        z_step = z(l+1)
                        SDL=SDL+Em(psirel, r_step, z_step)
c                       store cumulative sum for checks
                        sdl_cs(l+1) = sdl
D                       write (8,*) ' SdL increment is: ',Em(psirel), ' using psirel = ', psirel
                     endif
                 enddo
d                print*,'or 10 statement continue went here after first sdl=0'
            
C................INCLUDE OTHER ANGULAR FACTORS
            
D                write (8,*) ' after loop, xs,ys= ', xs, ys, ' xc, xd= ', 
D     .                       xc, xd, ' yc, yd= ', yc, yd, ' dalph, dbeta= ',
D     .                       dalph, dbeta, ' d, dist, s = ', d, dist, s
            
                 SOLD=SUM
d                print*,'sold=sum',sold
                 
c                calculcate the acceptance
c                for rectangular shape
c                detector x-direction
c                detector y-direction
c                 accept_x = accept(XC_bin, XD_bin, D, XTOT)
c                 accept_y = accept(YC_bin, YD_bin, D, YTOT)
c                 accept_tot = accept_x*accept_y
                 accept_tot = (PI*rcol(jdet)*rcdet(jdet)/nseg)**2/(D**2+xtot**2+ytot**2)
c                add sum for current orbit
                 SUM = SUM + SDL * accept_tot
c                calculate eff. for current orbit
c                S: orbit step size          
                 SUMEFF = SUM *  S / total_rate_sr
                 SNEW = SUM
                 SDEL = SNEW - SOLD 
d                print*,'sdel= snew-sold',sdel
d                print*, 'xd',xd
d                print*, 'yd',yd
d                print*, 's',s
D                print*,'sdv',sdv
                 EFFIC = SDEL  * S / total_rate_sr
            
D                 write (8,*) ' after loop, sold=', sold, 'snew=', snew,
D     .                       ' sdel=', sdel, ' sumeff=', sumeff, ' effic=', effic
            
            
c                store ofbit data, to be used later in the fitting proceedure
c     create output file name
c     i : coll. x-index
c     j : coll. y-index
c     id: det.  x-index
c     jdL det.  y-index
                 
                 write(orbit_id, '(i7)')  detector_number(jdet)*10000 + 100*i + id
c                 1000*i + 100*j + 10*id + jd
                 orbit_fname = TRIM(orbit_dir)//
     >                TRIM(orbit_head)//
     >                TRIM(ADJUSTL(orbit_id))//
     >                TRIM(orbit_tail)
                 print *, 'writing to: ', orbit_fname
                 call write_orbit(effic, accept_tot, sdel, sdv , n, jdet)
    
                 IF(EFFIC .LT. EFFLIM) then
                    PRINT 149, i, id, n, riptch, effic, EFFLIM
c                    j, id, jd, n, riptch, effic, EFFLIM
                 else
                    print 148, i, id, n, riptch, effic	
c                    j, id, jd, n, riptch, effic			
                 endif
c              enddo
c           enddo
        enddo
      enddo
c
c!!! Randomly throwing points on detector and collimator
c
c       DO I=1,81
cc      81 is number of trajectories, change later
c         call RANDOM_NUMBER(Rrand)
c         call RANDOM_NUMBER(Phirand)
c         call RANDOM_NUMBER(Rranc)
c         call RANDOM_NUMBER(Phiranc)
c         
c         XSd = XC*sqrt(Rrand)*cos(2.*PI*Phirand)
c         YSd = XC*sqrt(Rrand)*sin(2.*PI*Phirand)
c         XSc = XC*sqrt(Rranc)*cos(2.*PI*Phiranc)
c         YSc = XC*sqrt(Rranc)*sin(2.*PI*Phiranc)
cc     determine the direction of the line connecting the 
cc     center of the coll. bin and the center of the detector
c            XTOT=XSD - XSc
c            ALPH=ATAN(XTOT/D)
cD           write (8,*) ' xs= ', xs, ' xtot= ', xtot, ' alph= ', alph,
cD     .                 ' dalph= ', dalph, ' beold= ', beold
c
cc     WB bin entrance and detector in y-direction
cc                 center of the coll. bin and the center of the detector        
c                  YTOT = YSd - YSc
c                  BETA=ATAN(YTOT/D)
cc                 store the particle direction in the detector system
cc                   GYRO=ALPH
cc                  PITCH=BETA
c                  GYRO=0.
c                  PITCH=0.
cC                  print *, XAL, XS, XSD, XTOT, YBE, YS, YSD, YTOT
cD                 write (8,*) ' ys= ', ys, '0 ytot= ', ytot, ' beta= ',
cD     .                       beta, ' dbeta= ', dbeta, ' gyro= ', gyro, ' pitch= ', pitch
c            
cC.................INITIALIZE POSITION.
cc                 to be precise one should convert the xs/ys into toloridal coord to take the shift in the collimator
cc                 into account which is at the moment ignored
cc                  zs = 0.
cc  to start from detector instead of collimator opening put zs=-d
c                  zs = 0.                    
cc                 transformation from detector coordinate system to NSTX coordinate system and add to detector cwenter position
cc                 added rotation around z by phd angle                  
cc                 rotation angle should be changed to phd of probe (currently 79.3 in expressions below) 
c                  rt_br(1) = xsc*cp + ysc*sp*spph - zs*sp*cpph
c                  rt_br(2) = ysc*cpph + zs*spph
c                  rt_br(3) = xsc*sp - ysc*cp*spph + zs*cp*cpph
c                  rt(1) = rt_br(1)*cos(PI*79.3/180.0) - rt_br(2)*sin(PI*79.3/180.0) + rt0(1)
c                  rt(2) = rt_br(1)*sin(PI*79.3/180.0) + rt_br(2)*cos(PI*79.3/180.0) + rt0(2) 
c                  rt(3) = rt_br(3) + rt0(3)
cc     convert to toroidal coords (works only if phd is within +/- pi/2.
c                  rt_init(1) = sqrt(rt(1)**2 + rt(2)**2)
c                  rt_init(2) = asin(rt(2)/rt_init(1))
c                  rt_init(3) = rt(3)
c                
c                  DO K=1,3
cc                     R(K)=RINIT(K)
c                     R(K)=RT_INIT(K)
c                  enddo
c		
c            
cC.................CALCULATE INITIAL VELOCITIES (TIME-REVERSED).
cc                 setup the velocity vector in int the detector coord. system
c                  V(4)=1.
c                  DIST=SQRT(D**2 + XTOT**2 + YTOT**2)
c                  vx=XTOT/DIST
c                  vy=YTOT/DIST
c                  vz=SQRT(1. - vx**2 - vy**2)
cD                 write (8,*) ' vx, vy, vz=', vx, vy, vz
c            
cc                 transformation from detector coordinate system to NSTX coordinate system
c                  v(1) = vx*cp + vy*sp*spph - vz*sp*cpph
c                  v(2) = vy*cpph + vz*spph
c                  v(3) = vx*sp - vy*cp*spph + vz*cp*cpph
c            
c                  print *, 'detector v: ', vx, vy, vz
c                  print *, 'NSTX     v: ', v(1), v(2), v(3)
cC.................FIND ORBIT AND STORE IT IN X,Y,Z
c            
cD                 write (8,*) ' v= ', v
c            
cc                 maximal number of step to evaluate
c                  N=SSTP/S
c                  IF(N .GT. mxorpt) N=mxorpt
cd                 print*,'ready to call thal4 in subroutine chrien'
c            
cc                 N: number of real steps is returned from THAL4 
c                  CALL THAL4(N)
c            
cc                 no step could be calculated for this orbit
c                  IF(N.EQ.0) cycle
c            
cC.................CALCULATE SDL FOR THIS ORBIT
cC.................and accumulate flux at each position for later plotting
c            
c                  SDL=0.0d0
cc                 store the number of steps in the first element of the array steppsi
c                  steppsi(1) = n
cD                 write (8,*) 'Starting SdL calculation'
cc                 loop over the steps
c                  DO L=1,N
cc                    calculate psirel for current step, note that the psi data start
cc                    at index 2
c                     psirel = get_psirel(steppsi(l+1))
cD                    write (8,*) ' orbit step: ',l,' X,Z=',x(l+1),z(l+1),
cD     >                          ' flux=',steppsi(l+1),' psirel=',psirel
c               
cc                    psirel >=0. we are inside the plasma            
c                     IF (psirel .gt. 0.0d0) then
c                        r_step = x(l+1)
c                        z_step = z(l+1)
c                        SDL=SDL+Em(psirel, r_step, z_step)
cc                       store cumulative sum for checks
c                        sdl_cs(l+1) = sdl
cD                       write (8,*) ' SdL increment is: ',Em(psirel), ' using psirel = ', psirel
c                     endif
c                 enddo
cd                print*,'or 10 statement continue went here after first sdl=0'
c            
cC................INCLUDE OTHER ANGULAR FACTORS
c            
cD                write (8,*) ' after loop, xs,ys= ', xs, ys, ' xc, xd= ', 
cD     .                       xc, xd, ' yc, yd= ', yc, yd, ' dalph, dbeta= ',
cD     .                       dalph, dbeta, ' d, dist, s = ', d, dist, s
c            
c                 SOLD=SUM
cd                print*,'sold=sum',sold
c                 
cc                calculcate the acceptance
cc                for rectangular shape
cc                detector x-direction
cc                detector y-direction
cc                 accept_x = accept(XC_bin, XD_bin, D, XTOT)
cc                 accept_y = accept(YC_bin, YD_bin, D, YTOT)
cc                 accept_tot = accept_x*accept_y
ccc     
ccc                add sum for current orbit
cc                 SUM = SUM + SDL * accept_tot
ccc                calculate eff. for current orbit
ccc                S: orbit step size          
cc                 SUMEFF = SUM *  S / total_rate_sr
cc                 SNEW = SUM
cc                 SDEL = SNEW - SOLD 
ccd                print*,'sdel= snew-sold',sdel
ccd                print*, 'xd',xd
ccd                print*, 'yd',yd
ccd                print*, 's',s
ccD                print*,'sdv',sdv
cc                 EFFIC = SDEL  * S / total_rate_sr
cc            
ccD                 write (8,*) ' after loop, sold=', sold, 'snew=', snew,
ccD     .                       ' sdel=', sdel, ' sumeff=', sumeff, ' effic=', effic
c            
c            
cc                store ofbit data, to be used later in the fitting proceedure
cc     create output file name
cc     i : coll. x-index
cc     j : coll. y-index
cc     id: det.  x-index
cc     jdL det.  y-index
c                 
c                 write(orbit_id, '(i7)')  icounter*10000 + i
c                 orbit_fname = TRIM(orbit_dir)//
c     >                TRIM(orbit_head)//
c     >                TRIM(ADJUSTL(orbit_id))//
c     >                TRIM(orbit_tail)
c                 print *, 'writing to ', orbit_fname
c                 call write_orbit(effic, accept_tot, sdel, sdv , n, jdet)
c
c                 IF(EFFIC .LT. EFFLIM) then
c                    PRINT 149, i, j, id, jd, n, riptch, effic, EFFLIM
c                 else
c                    print 148, i, j, id, jd, n, riptch, effic			
c                 endif
c      enddo   
   
C......INCLUDE ALL THE CONSTANT FACTORS IN THE SUMMED EFFICIENCY      
      SUM = SUM * S/total_rate_sr
      PRINT 876, sum
 876  FORMAT(' Total efficiency of detector is: ',1pE12.3)
      
      RETURN
      
c 149  FORMAT(' i=', i6, ' j=', i6,  ' id=', i6, ' jd=', i6, ' n=', i6, ' Pitch angle=', f10.3,
 149  FORMAT(' i=', i6, ' id=', i6, ' n=', i6, ' Pitch angle=', f10.3,
     .     ' deg, effic=', 1pe11.3, 
     .     ' efflim=', e11.3, /, ' Efficiency less than lower limit, ',
     .     'so orbit will not be plotted')
c 148  FORMAT(' i=', i6, ' j=', i6,  ' id=', i6, ' jd=', i6, ' n=', i6, ' Pitch angle=', f10.3,
 148  FORMAT(' i=', i6, ' id=', i6, ' n=', i6, ' Pitch angle=', f10.3,
     .     ' deg, effic=', 1pe11.3)
      
      END
