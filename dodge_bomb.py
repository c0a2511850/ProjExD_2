import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0,-10),
    pg.K_DOWN: (0,+10),
    pg.K_LEFT: (-10,0),
    pg.K_RIGHT: (+10,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def get_kk_imgs(kk_img: pg.Surface) -> dict[tuple[int, int], pg.Surface]:
    hidari=kk_img
    migi=pg.transform.flip(hidari,True,False)
    kk_dict = {
        ( 0, 0):pg.transform.rotozoom(migi, 0, 1.0),
        ( 0, -5):pg.transform.rotozoom(migi, 90, 1.0),
        ( +5, -5):pg.transform.rotozoom(migi, 45, 1.0),
        ( +5, 0):pg.transform.rotozoom(migi, 0, 1.0),
        ( +5, +5):pg.transform.rotozoom(migi, -45, 1.0),
        ( 0, +5):pg.transform.rotozoom(migi, -90, 1.0),
        ( -5, +5):pg.transform.rotozoom(hidari, 45, 1.0),
        ( -5, 0):pg.transform.rotozoom(hidari, 0, 1.0),
        ( -5, -5):pg.transform.rotozoom(hidari, -45, 1.0),
    }
    return kk_dict

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面

    引数：画面Surface
    戻り値：なし
    """
    # 黒背景
    black = pg.Surface(screen.get_size())
    pg.Rect(0, 0, 1100, 650)
    black.set_alpha(200)

    if black.get_alpha() is None:
        black.set_alpha(200)

    # フォント
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = screen.get_rect().center

    # こうかとん画像（左）
    kk_img_left = pg.image.load("fig/8.png")
    kk_rct_left = kk_img_left.get_rect()

    # こうかとん画像（右）
    kk_img_right = pg.image.load("fig/8.png")
    kk_rct_right = kk_img_right.get_rect()

    # 配置（文字の左右）
    kk_rct_left.center = (text_rect.left - 100, text_rect.centery)
    kk_rct_right.center = (text_rect.right + 100, text_rect.centery)

    # 描画
    screen.blit(black, (0, 0))
    screen.blit(text, text_rect)
    screen.blit(kk_img_left, kk_rct_left)
    screen.blit(kk_img_right, kk_rct_right)

    pg.display.update()
    time.sleep(5)
def check_bound(rct):
    """
    引数：効果とんRectかばくだんRect
    戻り値：横方向、縦方向判定結果（True：画面内　False：画面外）
    """
    yoko, tate =True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255, 0, 0,),(10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    kk_rct = kk_img.get_rect()
    kk_hidari = pg.image.load("fig/3.png")
    kk_imgs = get_kk_imgs(kk_hidari)
    bb_rct = bb_img.get_rect()
    kk_rct.center = 300, 200
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            return # 衝突したらゲームオーバー
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate=check_bound(bb_rct)
        if not yoko:# 横方向判定
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

    
        
    

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
