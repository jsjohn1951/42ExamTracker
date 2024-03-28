NAME = FTEE

DEVSRC = ./dev.docker-compose.yml

PRODSRC = ./prod.docker-compose.yml

all : $(NAME)

$(NAME) : prod

dev :
	docker compose -f $(DEVSRC) up -d

prod :
	docker compose -f $(PRODSRC) up -d

clean :
	docker compose -f $(DEVSRC) down

fclean : clean
	docker builder prune -f

re : fclean all

.PHONY: all clean fclean re dev prod