MODULE BOPIX_EXTRA

	IMPLICIT NONE

	INTEGER:: BOK = 0
	INTEGER:: CLIK_LMAX
	REAL(4),DIMENSION(1:200,1:4):: CLIK_CL

END MODULE BOPIX_EXTRA
SUBROUTINE BOPIX_EXTRA_SET_LMAX(LMAX)
	USE BOPIX_EXTRA
	INTEGER,INTENT(IN)::LMAX
	CLIK_LMAX = LMAX
END SUBROUTINE 	BOPIX_EXTRA_SET_LMAX


SUBROUTINE BOPIX_EXTRA_ONLY_ONE(MOK)
	USE BOPIX_EXTRA
	INTEGER,INTENT(OUT)::MOK
	MOK = BOK
	BOK = 1
END SUBROUTINE 	BOPIX_EXTRA_ONLY_ONE


SUBROUTINE BOPIX_EXTRA_SET_BOPIX_NTHREADS(NT)
	USE BOPIX_EXTRA
	USE PARAMETER_MODULE
	INTEGER,INTENT(IN)::NT
   
	BOPIX_NTHREADS = NT
END SUBROUTINE 	BOPIX_EXTRA_SET_BOPIX_NTHREADS

SUBROUTINE BOPIX_EXTRA_FREE()
	USE BOPIX_EXTRA
	BOK =0
END SUBROUTINE 	BOPIX_EXTRA_FREE

SUBROUTINE BOPIX_EXTRA_LKL(LKL,CL)
	USE BOPIX_EXTRA
	USE BOPIX
	REAL(8),INTENT(OUT)::LKL
	REAL(4):: MENOLOGLIK_S 
	REAL(8),INTENT(IN),DIMENSION(0:4*CLIK_LMAX+3)::CL
	INTEGER::i,cur

	CLIK_CL=0
	!TT
	cur = 0
	DO i = 1,CLIK_LMAX
		CLIK_CL(i,1)=CL(cur+i)
	END DO	
	WRITE (*,*) "TT uu",CL(cur+2:cur+5)
	!EE
	cur = cur + CLIK_LMAX+1
	DO i = 1,CLIK_LMAX
		CLIK_CL(i,3)=CL(cur+i)
	END DO	
	WRITE (*,*) "EE uu",CL(cur+2:cur+5)
	!BB
	!cur = cur + CLIK_LMAX+1
	DO i = 1,CLIK_LMAX
		!CLIK_CL(i,3)=CL(cur+i)
		CLIK_CL(i,4)=0
	END DO	
	!TE
	cur = cur + CLIK_LMAX+1
	DO i = 1,CLIK_LMAX
		CLIK_CL(i,2)=CL(cur+i)
	END DO	
	WRITE (*,*) "TE uu",CL(cur+2:cur+5)
	
	WRITE (*,*) "TT aa",CLIK_CL(2:5,1)
	WRITE (*,*) "EE aa",CLIK_CL(2:5,3)
	WRITE (*,*) "BB aa",CLIK_CL(2:5,4)
	WRITE (*,*) "TE aa",CLIK_CL(2:5,2)
	
	
	CALL BOPIX_LIKELIHOOD(CLIK_CL,MENOLOGLIK_S)
	LKL = -MENOLOGLIK_S
END SUBROUTINE 	BOPIX_EXTRA_LKL

SUBROUTINE BOPIX_EXTRA_PARAMETER_INIT()
	USE BOPIX_EXTRA
	USE PARAMETER_MODULE
   
	CALL BOPIX_PARAMETER_INIT()
END SUBROUTINE 	BOPIX_EXTRA_PARAMETER_INIT
