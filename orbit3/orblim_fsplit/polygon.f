! This subroutine checks if the point lies inside the polygon
!
! 


          subroutine polygon(np, x_p, y_p, nd, x, y, results) 
          implicit none 
        
          ! number of polygon vertices
          integer, intent(in) :: np, nd
          
          ! polygon positions
          real*8, dimension(:), intent(in) :: x_p, y_p
          ! positions to test
          real*8, dimension(nd), intent(in) :: x, y
          ! polygon results
          integer*8, dimension(nd), intent(inout) :: results
        
          integer :: i, j, k, i1, j1
          integer :: inside
          
          real*8 :: p1x, p2x, p1y, p2y, xints
        
          results = 0
        
          do k = 1, nd
        
             ! n = len(poly)
             inside = 0
             
             p1x = x_p(1)
             p1y = y_p(1)
             ! this could go up to np + 2
             do i = 0, np+1
                ! i runs from 0 to np
                j = mod(i, np)
                ! shift indices to run start at 1
                j1 = j + 1
                i1 = i + 1
                p2x = x_p(j1)
                p2y = y_p(j1)
                ! is y larger than any of the two min. y-values ?
                if (y(k) > min(p1y,p2y)) then
                   ! if so is y smaller than any of the two max. y-values
                   if (y(k) <= max(p1y,p2y)) then
                      ! there is a potential that the point is inside 
                      if (x(k) <= max(p1x,p2x)) then
                         if ( p1y .ne. p2y) then
                            ! point not on a vertex calculate intersection with a horizontal line at y
                            xints = (y(k)-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                         endif
                         if ((p1x == p2x) .or. (x(k) <= xints)) then
                            inside = 1 - inside
                         endif
                      endif
                   endif
                endif
                p1x = p2x
                p1y = p2y
             enddo
             results(k) = inside
          enddo
        !  print *, results
          return 
           
        end subroutine polygon

