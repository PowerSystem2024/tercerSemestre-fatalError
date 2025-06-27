import pygame
import time

def show_game_over(screen, user_auth, username, final_score):
    global fondo_img
    fondo_img = pygame.transform.scale(pygame.image.load("assets/transicionNiveles/fondogameover.png"), (screen.get_width(), screen.get_height()))
    
    # Fuentes
    title_font = pygame.font.Font("assets/transicionNiveles/font5.ttf", 124)
    score_font = pygame.font.Font("assets/transicionNiveles/fonttexto.TTF", 42)
    info_font = pygame.font.Font("assets/transicionNiveles/fonttexto.TTF", 34)
    
    # Obtener datos del usuario
    user_data = user_auth.get_user_data(username)
    current_high_score = user_data.get("high_score", 0) if user_data else 0
    user_rank = user_auth.get_user_rank(username)
    best_score = user_auth.get_best_score()
    
    # Actualizar puntuación si es mejor
    if final_score > current_high_score:
        user_auth.update_high_score(username, final_score)
        new_record = True
    else:
        new_record = False
    
    waiting = True
    while waiting:
        # Limpiar pantalla
        screen.blit(fondo_img, (0, 0))
        
        LINE_SPACING = 38
        # Título
        text = title_font.render('GAME OVER', True, (255,0,0))
        shadow = title_font.render('GAME OVER', True, (40,0,0))
        text_rect = text.get_rect(center=(screen.get_width()//2, 130))
        shadow_rect = shadow.get_rect(center=(screen.get_width()//2+2, 132))
        screen.blit(shadow, shadow_rect)
        screen.blit(text, text_rect)
        y_offset = 250
        # Puntuación actual
        score_text = score_font.render(f'Puntuación Actual: {final_score}', True, (200,200,200))
        shadow = score_font.render(f'Puntuación Actual: {final_score}', True, (40,40,40))
        score_rect = score_text.get_rect(center=(screen.get_width()//2, y_offset))
        shadow_rect = shadow.get_rect(center=(screen.get_width()//2+1, y_offset+1))
        screen.blit(shadow, shadow_rect)
        screen.blit(score_text, score_rect)
        y_offset += LINE_SPACING
         # Ranking del usuario
        if user_rank:
            rank_text = score_font.render(f'Tu Ranking: #{user_rank}', True, (100, 180, 140))
            shadow = score_font.render(f'Tu Ranking: #{user_rank}', True, (0,80,80))
            rank_rect = rank_text.get_rect(center=(screen.get_width()//2, y_offset))
            shadow_rect = shadow.get_rect(center=(screen.get_width()//2+1, y_offset+1))
            screen.blit(shadow, shadow_rect)
            screen.blit(rank_text, rank_rect)
            y_offset += LINE_SPACING
        # Mejor puntuación personal
        if current_high_score > 0:
            high_score_text = score_font.render(f'Tu Mejor Puntuación: {current_high_score}', True, (255, 200, 50))
            shadow = score_font.render(f'Tu Mejor Puntuación: {current_high_score}', True, (80,80,0))
            high_score_rect = high_score_text.get_rect(center=(screen.get_width()//2, y_offset))
            shadow_rect = shadow.get_rect(center=(screen.get_width()//2+1, y_offset+1))
            screen.blit(shadow, shadow_rect)
            screen.blit(high_score_text, high_score_rect)
            y_offset += LINE_SPACING
        # Nuevo récord
        if new_record:
            new_record_text = score_font.render('¡NUEVO RÉCORD PERSONAL!', True, (0,255,0))
            shadow = score_font.render('¡NUEVO RÉCORD PERSONAL!', True, (0,80,0))
            new_record_rect = new_record_text.get_rect(center=(screen.get_width()//2, y_offset))
            shadow_rect = shadow.get_rect(center=(screen.get_width()//2+1, y_offset+1))
            screen.blit(shadow, shadow_rect)
            screen.blit(new_record_text, new_record_rect)
            y_offset += LINE_SPACING
       
        # Mejor puntuación global
        if best_score["high_score"] > 0:
            username = best_score["username"]
            if len(username) > 10:
                username = username[:10] + "..."
            global_best_text = score_font.render(
                f'Récord Global: {username} - {best_score["high_score"]}', 
                True, (255, 200, 50)
            )
            shadow = score_font.render(
                f'Récord Global: {username} - {best_score["high_score"]}', 
                True, (80,80,0)
            )
            global_best_rect = global_best_text.get_rect(center=(screen.get_width()//2, y_offset))
            shadow_rect = shadow.get_rect(center=(screen.get_width()//2+1, y_offset+1))
            screen.blit(shadow, shadow_rect)
            screen.blit(global_best_text, global_best_rect)
            y_offset += 38
        # Instrucciones
        info1 = info_font.render('Presiona R para reiniciar', True, (200, 200, 200))
        shadow = info_font.render('Presiona R para reiniciar', True, (40,40,40))
        info1_rect = info1.get_rect(center=(screen.get_width()//2, y_offset+30))
        shadow_rect = shadow.get_rect(center=(screen.get_width()//2+1, y_offset+31))
        screen.blit(shadow, shadow_rect)
        screen.blit(info1, info1_rect)
        info2 = info_font.render('Presiona L para ver ranking', True, (200, 200, 200))
        shadow = info_font.render('Presiona L para ver ranking', True, (40,40,40))
        info2_rect = info2.get_rect(center=(screen.get_width()//2, y_offset+60))
        shadow_rect = shadow.get_rect(center=(screen.get_width()//2+1, y_offset+61))
        screen.blit(shadow, shadow_rect)
        screen.blit(info2, info2_rect)
        info3 = info_font.render('Presiona ESC para salir', True, (200, 200, 200))
        shadow = info_font.render('Presiona ESC para salir', True, (40,40,40))
        info3_rect = info3.get_rect(center=(screen.get_width()//2, y_offset+90))
        shadow_rect = shadow.get_rect(center=(screen.get_width()//2+1, y_offset+91))
        screen.blit(shadow, shadow_rect)
        screen.blit(info3, info3_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_l:
                    # Mostrar ranking
                    from screens.leaderboard import show_leaderboard
                    show_leaderboard(screen, user_auth, username)
                if event.key == pygame.K_ESCAPE:
                    return False
    return False

import pygame

def render_text_fit_width(texto, font_path, color, max_width, initial_size, min_size=14):
    size = initial_size
    font = pygame.font.Font(font_path, size)
    text_surface = font.render(texto, True, color)
    while text_surface.get_width() > max_width and size > min_size:
        size -= 1
        font = pygame.font.Font(font_path, size)
        text_surface = font.render(texto, True, color)
    return text_surface, font

def show_victory(screen, user_auth, username, final_score):
    global fondo_img
    fondo_img = pygame.transform.scale(pygame.image.load("assets/transicionNiveles/imgvictoria.png"), (screen.get_width(), screen.get_height()))

    width = screen.get_width()
    max_text_width = width - 40  # margen de 20 px a cada lado
    
    waiting = True
    while waiting:
        screen.blit(fondo_img, (0, 0))
        
        pos_y = 169
        line_spacing = 50

        # Título
        title_text, title_font = render_text_fit_width('VICTORIA', "assets/transicionNiveles/font5.ttf", 	(100, 255, 100), max_text_width, 70)
        title_rect = title_text.get_rect(center=(width//2, pos_y))
        screen.blit(title_text, title_rect)
        pos_y += line_spacing * 2

        # Puntuación final
        score_str = f'Puntuación final: {final_score}'
        score_text, score_font = render_text_fit_width(score_str, "assets/transicionNiveles/fonttexto.TTF", (200,200,200), max_text_width, 34)
        score_rect = score_text.get_rect(center=(width//2, pos_y))
        screen.blit(score_text, score_rect)
        pos_y += line_spacing
        
        # Ranking del usuario
        user_rank = user_auth.get_user_rank(username)
        if user_rank:
            rank_str = f'Tu Ranking: #{user_rank}'
            rank_text, _ = render_text_fit_width(rank_str, "assets/transicionNiveles/fonttexto.TTF", (100, 180, 140), max_text_width, 34)
            rank_rect = rank_text.get_rect(center=(width//2, pos_y))
            screen.blit(rank_text, rank_rect)
            pos_y += line_spacing
            
        
        # Mejor puntuación personal
        user_data = user_auth.get_user_data(username)
        current_high_score = user_data.get("high_score", 0) if user_data else 0
        if current_high_score > 0:
            high_score_str = f'Tu mejor puntuación: {current_high_score}'
            high_score_text, _ = render_text_fit_width(high_score_str, "assets/transicionNiveles/fonttexto.TTF", (255, 200, 50), max_text_width, 34)
            high_score_rect = high_score_text.get_rect(center=(width//2, pos_y))
            screen.blit(high_score_text, high_score_rect)
            pos_y += line_spacing
        
        # Nuevo récord
        if final_score > current_high_score:
            new_record_text, _ = render_text_fit_width('¡NUEVO RÉCORD PERSONAL!', "assets/transicionNiveles/fonttexto.TTF", (0, 255, 0), max_text_width, 34)
            new_record_rect = new_record_text.get_rect(center=(width//2, pos_y))
            screen.blit(new_record_text, new_record_rect)
            pos_y += line_spacing
        
        
        
        # Mejor puntuación global
        best_score = user_auth.get_best_score()
        if best_score["high_score"] > 0:
            global_best_str = f'Récord Global: {best_score["username"]} - {best_score["high_score"]}'
            global_best_text, _ = render_text_fit_width(global_best_str, "assets/transicionNiveles/fonttexto.TTF", (255, 200, 50), max_text_width, 34)
            global_best_rect = global_best_text.get_rect(center=(width//2, pos_y))
            screen.blit(global_best_text, global_best_rect)
            pos_y += line_spacing
        
        # Instrucciones
        info_font = pygame.font.Font("assets/transicionNiveles/fonttexto.TTF", 28)
        info1 = info_font.render('Presiona L para ver ranking', True, (200, 200, 200))
        info2 = info_font.render('Presiona ESC para salir', True, (200, 200, 200))
        
        info1_rect = info1.get_rect(center=(width//2, pos_y + 10))
        info2_rect = info2.get_rect(center=(width//2, pos_y + 40))
        
        screen.blit(info1, info1_rect)
        screen.blit(info2, info2_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    from screens.leaderboard import show_leaderboard
                    show_leaderboard(screen, user_auth, username)
                if event.key == pygame.K_ESCAPE:
                    return False
    return False

