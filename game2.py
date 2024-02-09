import time
import pygame, sys, random


pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)        #dòng này để âm thanh mượt hơn
pygame.init()


manhinh = pygame.display.set_mode((900, 504))  #setup màn hình
tao_fps = pygame.time.Clock()
trongluc = 0.25
game_hoatdong = True
font_chu = pygame.font.Font('04B_19.TTF', 40)
diem = 0
diemcaonhat = 0
#tạo nền game
nen_game = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/nen.png').convert()   #ảnh nền game, conver để giảm dung lượng ảnh, load nhanh hơn
# nen_game = pygame.transform.scale2x(nen_game)   #làm cho nền game chiếm hết hàn hình
#tạo sàn game
san_game = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/floor.png').convert()   #ảnh sàn game
san_chay = 0    #Vị trí sàn chạy
#tạo chim
chim_duoi = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/yellowbird-downflap.png').convert_alpha()   #ảnh chim game, alpha để xóa khung đen quanh chim
chim_giua = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/yellowbird-midflap.png').convert_alpha()
chim_tren = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/yellowbird-upflap.png').convert_alpha()
danhsach_chim = [chim_duoi, chim_giua, chim_tren]    #0 1 2
chim_index = 0
chim = danhsach_chim[chim_index]
chim_hinhchunhat = chim.get_rect(center = (100, 50))          #Tạo hình chữ nhật quanh con chim, nhớ truyền vị trí(center, topleft, bottomright, midtop, midbottom)
chim_dichuyen = 0
#tạo đập cánh cho chim
chim_dapcanh = pygame.USEREVENT + 1     #+1 vì cho pygame biết đây là sự kiện thứ 2
pygame.time.set_timer(chim_dapcanh, 200)
#tạo ống
taoong = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/pipe-green.png').convert()   #ảnh ống game
# taoong = pygame.transform.scale2x(taoong)   #làm cho ống game chiếm hết hàn hình
danhsach_ong = []       #tạo list rỗng chứa ống
chieudai_ong = [200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450]      #chiều dài ngẫu nhiên của ống
#tạo timer
taoong_lientuc = pygame.USEREVENT       #làm xuất hiện ống liên tục
pygame.time.set_timer(taoong_lientuc, 1200)     #sau 1,2s sẽ tạo 1 ống mới
#Tạo màn hình kết thúc
game_over = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/message.png').convert_alpha()   #ảnh game over
game_over_hinhchunhat = game_over.get_rect(center = (450, 252))         #giao diện game over bằng 1 nửa màn hình game
game_over1 = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/gameover.png').convert_alpha()   #ảnh game over
game_over_hinhchunhat1 = game_over1.get_rect(center = (750, 50))
anhmeo = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/meow.jpg')  #ảnh game over
anhmeo_nho = pygame.transform.scale(anhmeo, (112, 190))
anhmeo_chunhat = anhmeo_nho.get_rect(center = (750, 250))

#chèn âm thanh
tieng_chimvocanh = pygame.mixer.Sound('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/sound/sfx_wing.wav')
tieng_vachamcot = pygame.mixer.Sound('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/sound/sfx_hit.wav')
tieng_ghidiem = pygame.mixer.Sound('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/sound/sfx_point.wav')
tieng_chimchet = pygame.mixer.Sound('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/sound/sfx_die.wav')
tieng_ghidiem_demnguoc = 100

def taonhieusan():
    manhinh.blit(san_game, (san_chay, 420))     #set tọa độ cho sàn game   , sàn 1
    manhinh.blit(san_game, (san_chay+335, 420))
    manhinh.blit(san_game, (san_chay+670, 420))
    manhinh.blit(san_game, (san_chay+1005, 420))

def tao_ong():
    ong_ngaunhien = random.choice(chieudai_ong)
    ong_duoi = taoong.get_rect(midtop = (1000, ong_ngaunhien))     #bao quanh ống bằng 1 nử chiều dài, rộng màn hình, ống xuất hiện ở vị trí x1000, y = ống ngãu nghiên
    ong_tren = taoong.get_rect(midtop=(1000, ong_ngaunhien-450))    #khoảng cách giữa 2 ống
    return ong_duoi, ong_tren


def dichuyenong(ongs):
    for ong in ongs:
        ong.centerx -=2            #ống vừa được tạo ra sẽ di chuyển về bên trái
    return ongs

def ve_ong(ongs):
    for ong in ongs:
        if ong.bottom >= 304:       #nếu ống lớn hơn màn hình cửa sổ game
            manhinh.blit(taoong, ong)
        else:
            latnguoc_ong = pygame.transform.flip(taoong , False, True)      #lật ngược óng, muốn lật chiều nào để True trục đó
            manhinh.blit(latnguoc_ong, ong)

def kiemtra_vacham(ongs):
    for ong in ongs:
        if chim_hinhchunhat.colliderect(ong):       #nếu chim va chạm ống sẽ hiển cảnh báo
            tieng_vachamcot.play()
            return False                            #nếu chim va chạm ống sẽ kết thúc
    if chim_hinhchunhat.top<=-75 or chim_hinhchunhat.bottom >= 420:     #nếu chim va chạm lên trên -75 và xuống dưới 420(bằng sàn) sẽ hiển cảnh báo
        tieng_chimchet.play()
        return False                                #nếu chim va chạm trên -75, dưới 420 sẽ kết thúc
    return True                                     #nếu chim khong va chạm trò chơi sẽ tiếp tục diễn ra

def xoay_chim(chim1):
    chim_moi = pygame.transform.rotozoom(chim1, -chim_dichuyen*3.4, 1)          #zotozoom tạo hiệu ứng xoay cho chim. biến chim1, xoay xuống dưới gấp 3.4 lần, kích cỡ 1
    return chim_moi

def chim_animation():       #tạo hiệu ứng đập cánh
    chim_moi = danhsach_chim[chim_index]
    chim_moi_hinhchunhat = chim_moi.get_rect(center =(100, chim_hinhchunhat.centery))
    return chim_moi, chim_moi_hinhchunhat


def update_diem(diem, diemcaonhat):
    if diem > diemcaonhat:
        diemcaonhat = diem
    return diemcaonhat

def diem_hienthi(tinhtrang):
    if tinhtrang == 'main game':
        diem_surface = font_chu.render(f'Score: {int(diem)}', True, (255, 255, 255))     #tạo giao diện điểm
        diem_hinhchunhat = diem_surface.get_rect(center = (450, 50))                          #tạo vị trí điểm
        manhinh.blit(diem_surface, diem_hinhchunhat)                                            #Hiển thị ra màn hình
    if tinhtrang == 'game_over':
        diem_surface = font_chu.render(f'Score: {int(diem)}', True, (255, 255, 255))     #tạo giao diện điểm
        diem_hinhchunhat = diem_surface.get_rect(center = (450, 50))                          #tạo vị trí điểm
        manhinh.blit(diem_surface, diem_hinhchunhat)

        diemcao_surface = font_chu.render(f'Hight score: {int(diemcaonhat)}', True, (255, 255, 255))     #tạo giao diện điểm cao nhất
        diemcao_hinhchunhat = diemcao_surface.get_rect(center = (450, 380))                          #tạo vị trí điểm cao nhất
        manhinh.blit(diemcao_surface, diemcao_hinhchunhat)


while True:
    for event in pygame.event.get():       #Tất cả sự kiện của game
        #Cục này để chọn được dấu X thoát game
        if event.type == pygame.QUIT:       #sự kiện Nếu người chơi nhấn vào chữ quit
            pygame.quit()                   #thì sẽ thoát game
            sys.exit()                      #Thoát hệ thống
        if event.type == pygame.KEYDOWN:   # sự kiện Khi có 1 phím được bấm xuống
            if event.key == pygame.K_SPACE or pygame.K_UP and game_hoatdong:  #chọn nút cách và nút lên sẽ nhảy chim với trạng thái game đang hoạt động
                chim_dichuyen = 0           #mỗi làn chim nhảy sẽ set trọng lực = 0
                chim_dichuyen = -6.5        #mỗi lần chim nhảy sẽ cho 1 lực hướng lên -y
                tieng_chimvocanh.play()
            if event.key == pygame.K_SPACE or pygame.K_UP and game_hoatdong==False:     #nếu game kết thúc, nhấn 1 phím bất kỳ game sẽ lại hoạt động
                game_hoatdong =True
                danhsach_ong.clear()        #Xóa hết danh sách ống đã được tạo trước đó
                chim_hinhchunhat.center = (100, 50)        #set lại hình chữ nhật quanh chim bằng mặc định
                chim_dichuyen = 0                           #set tọa độ chim bằng 0
                diem = 0                            #nếu chết sẽ reset diểm về 0
        if event.type == taoong_lientuc:    #sự kiện hiện ống liên tục
            danhsach_ong.extend(tao_ong())  #thêm tất cả các ống vào danh sách ống
        if event.type == chim_dapcanh:
            if chim_index <2:               #nếu chim index <2 thì sẽ cộng 1 mỗi lần đập cánh (chim dưới, giữa, trên)
                chim_index += 1
            else:
                chim_index = 0              #nếu chim indexx =2 thì reset index về 0(chim dưới)
            chim, chim_hinhchunhat == chim_animation()
    pygame.display.update()                 #để chữ quit hiện lên màn hình
    manhinh.blit(nen_game, (0, -70))     #set tọa độ cho nền game
    if game_hoatdong:
        #chim
        chim_dichuyen += trongluc               #chim di chuyển sẽ tăng trong lực   chim di chuyển xuống dưới = trọng lực
        chim_xoay = xoay_chim(chim)             #tạo hiệu ứng xoay cho chim
        chim_hinhchunhat.centery += chim_dichuyen    #chim di chuyển xuống dưới, hình chữ nhật quanh con chim cung di chuyển xuống dưới luôn
        manhinh.blit(chim_xoay, chim_hinhchunhat)   #cho chim ra màn hình
        game_hoatdong = kiemtra_vacham(danhsach_ong)            #nếu chim va chạm ống sẽ hiển cảnh báo
        #ống
        danhsach_ong = dichuyenong(danhsach_ong)    #lấy tất cả các ống được tạo ra và di chuyển sau đó sẽ trả lại danh sách ống mới
        ve_ong(danhsach_ong)                                #vẽ ống liên màn hình
        diem+=0.01
        diem_hienthi('main game')                              #Hiển thị điểm lên màn hình, nếu game hoạt độong thì hiển thị main game
        # tieng_ghidiem_demnguoc =-1                  #Mỗi lần chạy đc 1 điểm nó sẽ có tiếng cộng điêm
        # if tieng_ghidiem_demnguoc <=0:
        #     tieng_ghidiem.play()
        #     tieng_ghidiem_demnguoc =100
    else:
        manhinh.blit(game_over, game_over_hinhchunhat)
        manhinh.blit(game_over1, game_over_hinhchunhat1)
        manhinh.blit(anhmeo_nho, anhmeo_chunhat)
        diemcaonhat = update_diem(diem, diemcaonhat)
        diem_hienthi('game_over')                               #nếu game không hoạt động thì hiển thị game over


    #sàn
    san_chay -= 1                           #sàn sẽ chạy về vị trí bên trái
    taonhieusan()                           #gọi ra 3 sàn chạy
    if san_chay <= -335:                    #để sàn chạy vô hạn, nếu sàn đi qua vị trí -335 sẽ rết vị trí về 0
        san_chay = 0
    tao_fps.tick(100)                       #set FPS game, tốc độ game




