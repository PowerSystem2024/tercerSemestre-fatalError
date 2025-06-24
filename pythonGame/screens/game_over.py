import pygame
import time

def show_game_over(screen, user_auth, username, final_score):
    global fondo_img
    fondo_img = pygame.transform.scale(pygame.image.load("assets/transicionNiveles/fondonegro3.jpg"), (screen.get_width(), screen.get_height()))
    
    # Fuentes
    title_font = pygame.font.Font("assets/transicionNiveles/font2.ttf", 120)
    score_font = pygame.font.Font("assets/transicionNiveles/font4.TTF", 50)
    info_font = pygame.font.Font("assets/transicionNiveles/font4.TTF", 40)
    
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
        
        # Título
        text = title_font.render('GAME OVER', True, (255,0,0))
        text_rect = text.get_rect(center=(screen.get_width()//2, 150))
        screen.blit(text, text_rect)
        
        # Puntuación actual
        score_text = score_font.render(f'Puntuación: {final_score}', True, (255,255,255))
        score_rect = score_text.get_rect(center=(screen.get_width()//2, 280))
        screen.blit(score_text, score_rect)
        
        # Mejor puntuación personal
        if current_high_score > 0:
            high_score_text = score_font.render(f'Tu mejor: {current_high_score}', True, (255,255,0))
            high_score_rect = high_score_text.get_rect(center=(screen.get_width()//2, 330))
            screen.blit(high_score_text, high_score_rect)
        
        # Nuevo récord
        if new_record:
            new_record_text = score_font.render('¡NUEVO RÉCORD PERSONAL!', True, (0,255,0))
            new_record_rect = new_record_text.get_rect(center=(screen.get_width()//2, 380))
            screen.blit(new_record_text, new_record_rect)
        
        # Ranking del usuario
        if user_rank:
            rank_text = score_font.render(f'Tu posición: #{user_rank}', True, (0,255,255))
            rank_rect = rank_text.get_rect(center=(screen.get_width()//2, 430))
            screen.blit(rank_text, rank_rect)
        
        # Mejor puntuación global
        if best_score["high_score"] > 0:
            global_best_text = score_font.render(
                f'Récord mundial: {best_score["username"]} - {best_score["high_score"]}', 
                True, (255,215,0)
            )
            global_best_rect = global_best_text.get_rect(center=(screen.get_width()//2, 480))
            screen.blit(global_best_text, global_best_rect)
        
        # Instrucciones
        info1 = info_font.render('Presiona R para reiniciar', True, (255,255,255))
        info2 = info_font.render('Presiona L para ver ranking', True, (255,255,255))
        info3 = info_font.render('Presiona ESC para salir', True, (255,255,255))
        
        info1_rect = info1.get_rect(center=(screen.get_width()//2, 550))
        info2_rect = info2.get_rect(center=(screen.get_width()//2, 590))
        info3_rect = info3.get_rect(center=(screen.get_width()//2, 630))
        
        screen.blit(info1, info1_rect)
        screen.blit(info2, info2_rect)
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

def show_victory(screen, user_auth, username, final_score):
    global fondo_img
    fondo_img = pygame.transform.scale(pygame.image.load("assets/transicionNiveles/fondonegro3.jpg"), (screen.get_width(), screen.get_height()))
    
    # Fuentes
    title_font = pygame.font.Font("assets/transicionNiveles/font2.ttf", 120)
    score_font = pygame.font.Font("assets/transicionNiveles/font4.TTF", 50)
    info_font = pygame.font.Font("assets/transicionNiveles/font4.TTF", 40)
    
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
        
        # Título
        text = title_font.render('VICTORIA', True, (0,255,0))
        text_rect = text.get_rect(center=(screen.get_width()//2, 150))
        screen.blit(text, text_rect)
        
        # Puntuación final
        score_text = score_font.render(f'Puntuación final: {final_score}', True, (255,255,255))
        score_rect = score_text.get_rect(center=(screen.get_width()//2, 280))
        screen.blit(score_text, score_rect)
        
        # Mejor puntuación personal
        if current_high_score > 0:
            high_score_text = score_font.render(f'Tu mejor: {current_high_score}', True, (255,255,0))
            high_score_rect = high_score_text.get_rect(center=(screen.get_width()//2, 330))
            screen.blit(high_score_text, high_score_rect)
        
        # Nuevo récord
        if new_record:
            new_record_text = score_font.render('¡NUEVO RÉCORD PERSONAL!', True, (0,255,0))
            new_record_rect = new_record_text.get_rect(center=(screen.get_width()//2, 380))
            screen.blit(new_record_text, new_record_rect)
        
        # Ranking del usuario
        if user_rank:
            rank_text = score_font.render(f'Tu posición: #{user_rank}', True, (0,255,255))
            rank_rect = rank_text.get_rect(center=(screen.get_width()//2, 430))
            screen.blit(rank_text, rank_rect)
        
        # Mejor puntuación global
        if best_score["high_score"] > 0:
            global_best_text = score_font.render(
                f'Récord mundial: {best_score["username"]} - {best_score["high_score"]}', 
                True, (255,215,0)
            )
            global_best_rect = global_best_text.get_rect(center=(screen.get_width()//2, 480))
            screen.blit(global_best_text, global_best_rect)
        
        # Instrucciones
        info1 = info_font.render('Presiona L para ver ranking', True, (255,255,255))
        info2 = info_font.render('Presiona ESC para salir', True, (255,255,255))
        
        info1_rect = info1.get_rect(center=(screen.get_width()//2, 550))
        info2_rect = info2.get_rect(center=(screen.get_width()//2, 590))
        
        screen.blit(info1, info1_rect)
        screen.blit(info2, info2_rect)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    # Mostrar ranking
                    from screens.leaderboard import show_leaderboard
                    show_leaderboard(screen, user_auth, username)
                if event.key == pygame.K_ESCAPE:
                    return False
    return False
