import pygame

def show_leaderboard(screen, user_auth, current_username=None):
    """Mostrar pantalla del top 10 de puntuaciones"""
    
    # Cargar fondo
    fondo_img = pygame.transform.scale(
        pygame.image.load("assets/mapa/MENU.png"), 
        (screen.get_width(), screen.get_height())
    )
    
    # Fuentes
    title_font = pygame.font.Font("assets/transicionNiveles/font8.otf", 51)
    header_font = pygame.font.Font("assets/transicionNiveles/fonttexto.TTF", 28)
    score_font = pygame.font.Font("assets/transicionNiveles/fonttexto.TTF", 22)
    info_font = pygame.font.Font("assets/transicionNiveles/fonttexto.TTF", 20)
    
    # Obtener datos
    top_scores = user_auth.get_top_10_scores()
    best_score = user_auth.get_best_score()
    user_rank = user_auth.get_user_rank(current_username) if current_username else None
    
    waiting = True
    while waiting:
        # Limpiar pantalla
        screen.blit(fondo_img, (0, 0))
        
        # Título
        title_text = title_font.render('TOP 10 PUNTUACIONES', True, (204, 102, 0))
        shadow = title_font.render('TOP 10 PUNTUACIONES', True, (40, 40, 0))
        title_rect = title_text.get_rect(center=(screen.get_width()//2, 60))
        shadow_rect = shadow.get_rect(center=(screen.get_width()//2+2, 62))
        screen.blit(shadow, shadow_rect)
        screen.blit(title_text, title_rect)
        y_offset = 110
        # Mejor puntuación global
        if best_score["high_score"] > 0:
            best_text = header_font.render(f'Mejor Puntuación: {best_score["username"]} - {best_score["high_score"]}', True, (255, 200, 50))
            shadow = header_font.render(f'Mejor Puntuación: {best_score["username"]} - {best_score["high_score"]}', True, (80, 80, 0))
            best_rect = best_text.get_rect(center=(screen.get_width()//2, y_offset))
            shadow_rect = shadow.get_rect(center=(screen.get_width()//2+1, y_offset+1))
            screen.blit(shadow, shadow_rect)
            screen.blit(best_text, best_rect)
            y_offset += 40
        # Ranking del usuario actual
        if current_username and user_rank:
            rank_text = header_font.render(f'Tu posición: #{user_rank}', True, (100, 180, 140))
            shadow = header_font.render(f'Tu posición: #{user_rank}', True, (0, 80, 80))
            rank_rect = rank_text.get_rect(center=(screen.get_width()//2, y_offset))
            shadow_rect = shadow.get_rect(center=(screen.get_width()//2+1, y_offset+1))
            screen.blit(shadow, shadow_rect)
            screen.blit(rank_text, rank_rect)
            y_offset += 36
        # Lista del top 10
        y_start = y_offset + 10
        line_height = 30
        for i, score_data in enumerate(top_scores):
            color = (0, 255, 0) if (current_username and score_data["username"] == current_username) else (255, 255, 255)
            if i == 0:
                position = "🥇"
            elif i == 1:
                position = "🥈"
            elif i == 2:
                position = "🥉"
            else:
                position = f"#{i+1}"
            username = score_data["username"]
            if len(username) > 10:
                username = username[:10] + "..."
            text_line = f'{position} {username} - {score_data["high_score"]}'
            shadow = score_font.render(text_line, True, (40,40,40))
            score_text = score_font.render(text_line, True, color)
            score_rect = score_text.get_rect(center=(screen.get_width()//2, y_start + i * line_height))
            shadow_rect = shadow.get_rect(center=(screen.get_width()//2+1, y_start + i * line_height+1))
            screen.blit(shadow, shadow_rect)
            screen.blit(score_text, score_rect)
        
        # Instrucciones
        if len(top_scores) == 0:
            no_scores_text = score_font.render(
                'No hay puntuaciones registradas aún', 
                True, (128, 128, 128)
            )
            no_scores_rect = no_scores_text.get_rect(center=(screen.get_width()//2, y_start + 100))
            screen.blit(no_scores_text, no_scores_rect)
        
        # Instrucciones de salida
        exit_text = info_font.render('Presiona ESC para volver', True, (200, 200, 200))
        shadow = info_font.render('Presiona ESC para volver', True, (40,40,40))
        exit_rect = exit_text.get_rect(center=(screen.get_width()//2, screen.get_height() - 62))
        shadow_rect = shadow.get_rect(center=(screen.get_width()//2+1, screen.get_height() - 61))
        screen.blit(shadow, shadow_rect)
        screen.blit(exit_text, exit_rect)
        
        pygame.display.flip()
        
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
    
    return True 