import pygame

def show_leaderboard(screen, user_auth, current_username=None):
    """Mostrar pantalla del top 10 de puntuaciones"""
    
    # Cargar fondo
    fondo_img = pygame.transform.scale(
        pygame.image.load("assets/transicionNiveles/fondonegro3.jpg"), 
        (screen.get_width(), screen.get_height())
    )
    
    # Fuentes
    title_font = pygame.font.Font("assets/transicionNiveles/font2.ttf", 80)
    header_font = pygame.font.Font("assets/transicionNiveles/font4.TTF", 40)
    score_font = pygame.font.Font("assets/transicionNiveles/font4.TTF", 35)
    info_font = pygame.font.Font("assets/transicionNiveles/font4.TTF", 30)
    
    # Obtener datos
    top_scores = user_auth.get_top_10_scores()
    best_score = user_auth.get_best_score()
    user_rank = user_auth.get_user_rank(current_username) if current_username else None
    
    waiting = True
    while waiting:
        # Limpiar pantalla
        screen.blit(fondo_img, (0, 0))
        
        # Título
        title_text = title_font.render('TOP 10 PUNTUACIONES', True, (255, 215, 0))  # Dorado
        title_rect = title_text.get_rect(center=(screen.get_width()//2, 80))
        screen.blit(title_text, title_rect)
        
        # Mejor puntuación global
        if best_score["high_score"] > 0:
            best_text = header_font.render(
                f'🏆 MEJOR MARCA: {best_score["username"]} - {best_score["high_score"]}', 
                True, (255, 255, 0)  # Amarillo
            )
            best_rect = best_text.get_rect(center=(screen.get_width()//2, 140))
            screen.blit(best_text, best_rect)
        
        # Ranking del usuario actual
        if current_username and user_rank:
            rank_text = header_font.render(
                f'Tu posición: #{user_rank}', 
                True, (0, 255, 255)  # Cyan
            )
            rank_rect = rank_text.get_rect(center=(screen.get_width()//2, 180))
            screen.blit(rank_text, rank_rect)
        
        # Lista del top 10
        y_start = 240
        for i, score_data in enumerate(top_scores):
            # Color especial para el usuario actual
            if current_username and score_data["username"] == current_username:
                color = (0, 255, 0)  # Verde para el usuario actual
            else:
                color = (255, 255, 255)  # Blanco para otros
            
            # Número de posición con emoji
            if i == 0:
                position = "🥇"
            elif i == 1:
                position = "🥈"
            elif i == 2:
                position = "🥉"
            else:
                position = f"#{i+1}"
            
            score_text = score_font.render(
                f'{position} {score_data["username"]} - {score_data["high_score"]}', 
                True, color
            )
            score_rect = score_text.get_rect(center=(screen.get_width()//2, y_start + i * 45))
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
        exit_text = info_font.render(
            'Presiona ESC para volver', 
            True, (200, 200, 200)
        )
        exit_rect = exit_text.get_rect(center=(screen.get_width()//2, screen.get_height() - 50))
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