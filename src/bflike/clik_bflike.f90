MODULE BFLIKE_EXTRA

  IMPLICIT NONE

  INTEGER:: CLIK_LMAX,CLIK_LMIN
  real(8),dimension(2:1000,6) :: cltt
  real(8),parameter:: PI    = 3.141592653589793238462643383279502884197
  integer::bok
  
END MODULE BFLIKE_EXTRA

SUBROUTINE BFLIKE_EXTRA_ONLY_ONE(MOK)
  USE BFLIKE_EXTRA
  INTEGER,INTENT(OUT)::MOK
  MOK = BOK
  BOK = 1
END SUBROUTINE  BFLIKE_EXTRA_ONLY_ONE

SUBROUTINE BFLIKE_EXTRA_FREE()
  USE BFLIKE_EXTRA
  use bflike
  call clean_pix_like
  BOK =0
END SUBROUTINE  BFLIKE_EXTRA_FREE


SUBROUTINE BFLIKE_EXTRA_LKL(LKL,CL)
  use bflike
  use BFLIKE_EXTRA
  
  REAL(8),INTENT(OUT)::LKL
  REAL(8),INTENT(IN),DIMENSION(0:(CLIK_LMAX-CLIK_LMIN)*6)::CL
  INTEGER::i,cur

  
  cur = 0
  cltt = 0
  !TT
  DO i = clik_lmin,clik_lmax
    cltt(i,myTT)=CL(cur)*(i*(i+1.))/2./PI
    cur = cur + 1
  END DO  
  !EE
  DO i = clik_lmin,clik_lmax
    cltt(i,myEE)=CL(cur)*(i*(i+1.))/2./PI
    cur = cur + 1
  END DO  
  !BB
  DO i = clik_lmin,clik_lmax
    cltt(i,myBB)=CL(cur)*(i*(i+1.))/2./PI
    cur = cur + 1
  END DO  
  !TE
  DO i = clik_lmin,clik_lmax
    cltt(i,myTE)=CL(cur)*(i*(i+1.))/2./PI
    cur = cur + 1
  END DO  
  !TB
  DO i = clik_lmin,clik_lmax
    cltt(i,myTB)=CL(cur)*(i*(i+1.))/2./PI
    cur = cur + 1
  END DO  
  !EB
  DO i = clik_lmin,clik_lmax
    cltt(i,myEB)=CL(cur)*(i*(i+1.))/2./PI
    cur = cur + 1
  END DO  
  call get_pix_loglike(cltt,LKL)

END SUBROUTINE  BFLIKE_EXTRA_LKL

SUBROUTINE BFLIKE_EXTRA_PARAMETER_INIT(datadir,l_datadir,lmin,lmax)
  use bflike
  use BFLIKE_EXTRA
  
  INTEGER,INTENT(IN)::l_datadir,lmin,lmax
  character(len=l_datadir)::datadir

  call init_pix_like(TRIM(datadir))
  
  clik_lmin = lmin
  clik_lmax = lmax
    
END SUBROUTINE  BFLIKE_EXTRA_PARAMETER_INIT