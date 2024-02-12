NAME = FTEE

SRC = ./docker-compose.yml

all : $(NAME)

$(NAME) :
	docker compose -f $(SRC) up -d

clean :
	docker compose -f $(SRC) down

fclean : clean
	docker builder prune -f

re : fclean all

.PHONY: all clean fclean re