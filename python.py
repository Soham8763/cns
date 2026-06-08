//Timber
#include <SFML/Graphics.hpp>
#include <SFML/Audio.hpp>
#include <ctime>
#include <sstream>

using namespace sf;
using namespace std;

enum class side { LEFT, RIGHT, NONE };

const int NUM_BRANCHES = 6;
side branchpositions[NUM_BRANCHES];

// 🌿 Updates branch positions
void updateBranches(int seed) {
    for (int i = NUM_BRANCHES - 1; i > 0; i--) {
        branchpositions[i] = branchpositions[i - 1];
    }

    int r = rand() % 5;

    if (r == 0) branchpositions[0] = side::LEFT;
    else if (r == 1) branchpositions[0] = side::RIGHT;
    else branchpositions[0] = side::NONE;
}

int main() {
    srand(time(0));

    VideoMode vm(1920, 1080);
    RenderWindow window(vm, "TIMBER");

    View view(FloatRect(0, 0, 1920, 1080));
    window.setView(view);

    // =========================
    // 🔊 SOUND SETUP
    // =========================

    // Sound buffers (load audio files into memory -> Chop, Death, OOT)
    SoundBuffer chopBuffer;
    SoundBuffer deathBuffer;
    SoundBuffer ootBuffer;

    chopBuffer.loadFromFile("chop.wav");
    deathBuffer.loadFromFile("death.wav");
    ootBuffer.loadFromFile("out_of_time.wav");

    // Sound objects (used to actually play sounds)
    Sound chop;
    Sound death;
    Sound outOfTime;

    chop.setBuffer(chopBuffer);
    death.setBuffer(deathBuffer);
    outOfTime.setBuffer(ootBuffer);

    // =========================
    // GRAPHICS SETUP
    // =========================

    Texture textureBackground;
    textureBackground.loadFromFile("background.png");
    Sprite spriteBackground(textureBackground);

    Texture textureTree;
    textureTree.loadFromFile("tree.png");
    Sprite spriteTree(textureTree);
    spriteTree.setScale(300.0f / textureTree.getSize().x,
                        900.0f / textureTree.getSize().y);
    spriteTree.setPosition(810, 0);

    // 🌥️ Clouds
    Texture textureCloud;
    textureCloud.loadFromFile("cloud.png");

    Sprite spriteCloud1(textureCloud);
    Sprite spriteCloud2(textureCloud);
    Sprite spriteCloud3(textureCloud);

    bool cloud1Active = false, cloud2Active = false, cloud3Active = false;
    float cloud1Speed = 0, cloud2Speed = 0, cloud3Speed = 0;

    // 🐝 Bee
    Texture textureBee;
    textureBee.loadFromFile("bee.png");
    Sprite spriteBee(textureBee);
    bool beeActive = false;
    float beeSpeed = 0;

    // 🌿 Branches
    Texture textureBranch;
    textureBranch.loadFromFile("branch.png");
    Sprite branch[NUM_BRANCHES];

    for (int i = 0; i < NUM_BRANCHES; i++) {
        branch[i].setTexture(textureBranch);
        branch[i].setOrigin(220, 20);
        branch[i].setPosition(-2000, -2000);
        branchpositions[i] = side::NONE;
    }

    // 🧍 Player
    Texture texturePlayer;
    texturePlayer.loadFromFile("player.png");
    Sprite spritePlayer(texturePlayer);
    spritePlayer.setPosition(580, 720);

    // 💀 RIP
    Texture textureRip;
    textureRip.loadFromFile("rip.png");
    Sprite spriteRip(textureRip);
    spriteRip.setPosition(600, 2000);

    // 🪓 Axe
    Texture textureAxe;
    textureAxe.loadFromFile("axe.png");
    Sprite spriteAxe(textureAxe);
    spriteAxe.setPosition(700, 830);

    // 🪵 Log
    Texture textureLog;
    textureLog.loadFromFile("log.png");
    Sprite spriteLog(textureLog);
    spriteLog.setPosition(810, 720);

    bool logActive = false;
    float logSpeedX = 0;
    float logSpeedY = 0;

    // INPUT
    bool acceptInput = false;

    // ⏳ Time bar
    RectangleShape timeBar;
    float timeBarStartWidth = 400;
    float timeRemaining = 6.0f;
    float timeBarHeight = 30;
    float timeBarWidthPerSecond = timeBarStartWidth / timeRemaining;

    timeBar.setSize(Vector2f(timeBarStartWidth, timeBarHeight));
    timeBar.setFillColor(Color::Red);
    timeBar.setPosition((1920 - timeBarStartWidth) / 2.0f, 1020);

    // 📝 Text
    Font font;
    font.loadFromFile("KOMIKAP_.ttf");

    Text messageText("Press Enter to start", font, 75);
    messageText.setPosition(600, 500);

    Text scoreText("", font, 60);
    scoreText.setPosition(20, 20);

    int score = 0;
    bool paused = true;

    Clock clock;

    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed)
                window.close();
        }

        if (Keyboard::isKeyPressed(Keyboard::Escape))
            window.close();

        // ▶️ START GAME
        static bool enterReleased = true;

        if (paused) {
            if (Keyboard::isKeyPressed(Keyboard::Enter) && enterReleased) {
                enterReleased = false;

                paused = false;
                score = 0;
                timeRemaining = 6.0f;

                for (int i = 0; i < NUM_BRANCHES; i++)
                    branchpositions[i] = side::NONE;

                spritePlayer.setPosition(580, 720);
                spriteRip.setPosition(600, 2000);

                acceptInput = true;
                clock.restart();
            }

            if(!Keyboard::isKeyPressed(Keyboard::Enter)) {
                enterReleased = true;
            }
        }

        // =========================
        // 🎮 PLAYER INPUT
        // =========================
        if (acceptInput && !paused) {
            // 👉 RIGHT CHOP
            if (Keyboard::isKeyPressed(Keyboard::Right)) {
                spritePlayer.setPosition(1200, 720);
                spriteAxe.setPosition(1075, 830);
                score++;
                timeRemaining += (2.0f / score) + 0.15f;
                chop.play();  // 🔊 play chop sound
                spriteLog.setPosition(810, 720);
                logSpeedX = -5000;
                logSpeedY = -1500;
                logActive = true;
                updateBranches(score);
                // 💀 Death check
                if (branchpositions[5] == side::RIGHT) {
                    paused = true;
                    acceptInput = false;
                    messageText.setString("DED!");
                    spriteRip.setPosition(580, 720);
                    spritePlayer.setPosition(2000, 720);
                    death.play(); // 🔊 play death sound
                }
                acceptInput = false;
            }

            // 👉 LEFT CHOP
            if (Keyboard::isKeyPressed(Keyboard::Left)) {
                spritePlayer.setPosition(580, 720);
                spriteAxe.setPosition(700, 830);

                score++;
                timeRemaining += (2.0f / score) + 0.15f;

                chop.play();  // 🔊 play chop sound

                spriteLog.setPosition(810, 720);
                logSpeedX = 5000;
                logSpeedY = -1500;
                logActive = true;

                updateBranches(score);

                if (branchpositions[5] == side::LEFT) {
                    paused = true;
                    acceptInput = false;
                    messageText.setString("DED!");
                    spriteRip.setPosition(580, 720);
                    spritePlayer.setPosition(2000, 720);

                    death.play(); // 🔊 play death sound
                }

                acceptInput = false;
            }
        }

        // RESET INPUT
        if (!Keyboard::isKeyPressed(Keyboard::Left) &&
            !Keyboard::isKeyPressed(Keyboard::Right)) {
            acceptInput = true;
        }

        if (!paused) {
            Time dt = clock.restart();

            // ⏳ TIME LOGIC
            timeRemaining -= dt.asSeconds();

            if (timeRemaining <= 0.0f) {
                paused = true;
                messageText.setString("Out of time!");
                outOfTime.play(); // 🔊 out of time sound
            }

            if (timeRemaining > 6.0f) timeRemaining = 6.0f;

            timeBar.setSize(Vector2f(timeBarWidthPerSecond * timeRemaining,
                                     timeBarHeight));

            // 🐝 Bee movement
            if (!beeActive) {
                beeSpeed = rand() % 200 + 200;
                spriteBee.setPosition(2000, rand() % 400 + 200);
                beeActive = true;
            } else {
                spriteBee.move(-beeSpeed * dt.asSeconds(), 0);
                if (spriteBee.getPosition().x < -100)
                    beeActive = false;
            }

            // ☁ Clouds movement
            if (!cloud1Active) {
                cloud1Speed = rand() % 200 + 50;
                spriteCloud1.setPosition(-200, rand() % 150);
                cloud1Active = true;
            } else {
                spriteCloud1.move(cloud1Speed * dt.asSeconds(), 0);
                if (spriteCloud1.getPosition().x > 1920)
                    cloud1Active = false;
            }

            if (!cloud2Active) {
                cloud2Speed = rand() % 200 + 50;
                spriteCloud2.setPosition(-200, rand() % 300);
                cloud2Active = true;
            } else {
                spriteCloud2.move(cloud2Speed * dt.asSeconds(), 0);
                if (spriteCloud2.getPosition().x > 1920)
                    cloud2Active = false;
            }

            if (!cloud3Active) {
                cloud3Speed = rand() % 200 + 50;
                spriteCloud3.setPosition(-200, rand() % 450);
                cloud3Active = true;
            } else {
                spriteCloud3.move(cloud3Speed * dt.asSeconds(), 0);
                if (spriteCloud3.getPosition().x > 1920)
                    cloud3Active = false;
            }

            // 🪵 LOG movement
            if (logActive) {
                spriteLog.move(logSpeedX * dt.asSeconds(),
                               logSpeedY * dt.asSeconds());

                if (spriteLog.getPosition().x < -100 ||
                    spriteLog.getPosition().x > 2000) {
                    logActive = false;
                    spriteLog.setPosition(810, 720);
                }
            }
        }

        // 🧮 Score display
        stringstream ss;
        ss << "Score = " << score;
        scoreText.setString(ss.str());

        // 🌿 Branch positioning
        for (int i = 0; i < NUM_BRANCHES; i++) {
            float height = i * 150;

            if (branchpositions[i] == side::LEFT) {
                branch[i].setPosition(610, height);
                branch[i].setRotation(180);
            } else if (branchpositions[i] == side::RIGHT) {
                branch[i].setPosition(1330, height);
                branch[i].setRotation(0);
            } else {
                branch[i].setPosition(3000, height);
            }
        }

        // 🎨 DRAW EVERYTHING
        window.clear();

        window.draw(spriteBackground);
        window.draw(spriteCloud1);
        window.draw(spriteCloud2);
        window.draw(spriteCloud3);
        window.draw(spriteTree);
        window.draw(spriteBee);
        window.draw(spritePlayer);
        window.draw(spriteAxe);
        window.draw(spriteLog);
        window.draw(spriteRip);

        for (int i = 0; i < NUM_BRANCHES; i++)
            window.draw(branch[i]);

        window.draw(scoreText);
        window.draw(timeBar);

        if (paused)
            window.draw(messageText);

        window.display();
    }
    return 0;
}

// Pong

#include <SFML/Graphics.hpp>
#include <sstream>
#include "bat.h"
#include "ball.h"
#include <cstdlib>

using namespace sf;
using namespace std;

int main(){
    VideoMode vm(1920, 1080);
    RenderWindow window(vm, "PONG");

    View view(FloatRect(0, 0, 1920, 1080));
    window.setView(view);

    int score = 0;
    int lives = 3;

    Font font;
    font.loadFromFile("KOMIKAP_.ttf");

    Text hud;
    hud.setFont(font);
    hud.setCharacterSize(64);
    hud.setFillColor(Color::White);

    Bat bat(1920 / 2, 1080 - 20);
    Ball ball(1920 / 2 - 10, 0);

    float x = (rand() % 200 - 100);
    if(x == 0) x = 50;
    float y = 100.0f;
    ball.setDirection(x, y);

    Clock clock;
    while(window.isOpen()){
        Event event;

        while(window.pollEvent(event)){
            if(event.type == Event::Closed){
                window.close();
            }
        }

        if(Keyboard::isKeyPressed(Keyboard::Escape)){
            window.close();
        }

        Time dt = clock.restart();

        if(Keyboard::isKeyPressed(Keyboard::Left)){
            bat.moveLeft();
        } else {
            bat.stopLeft();
        }
        if(Keyboard::isKeyPressed(Keyboard::Right)){
            bat.moveRight();
        } else {
            bat.stopRight();
        }

        bat.update(dt);
        ball.update(dt);

        Vector2f pos = ball.getShape().getPosition();
        float radius = ball.getShape().getRadius();

        // Wall collision
        // Left wall
        if(pos.x <= 0){
            ball.reboundSides();
            pos.x = 0;
        }

        // Right wall
        if(pos.x + radius * 2 >= 1920){
            ball.reboundSides();
            pos.x = 1920 - radius * 2;
        }

        // Top wall
        if(pos.y <= 0){
            ball.reboundTopBottom();
            pos.y = 0;
        }

        ball.setPosition(pos.x, pos.y);

       //Bat collision
        if(ball.getShape().getGlobalBounds().intersects(bat.getShape().getGlobalBounds())){
            float batCenter = bat.getShape().getPosition().x + bat.getShape().getSize().x / 2;
            float ballCenter = ball.getShape().getPosition().x + radius;

            float distance = ballCenter - batCenter;

            float percent = distance / (bat.getShape().getSize().x / 2);

            ball.setDirection(percent * 200, -100);

            // reposition ball above bat
            pos.y = bat.getShape().getPosition().y - radius * 2;
            ball.setPosition(pos.x, pos.y);

            score++;
        }

        //handling bottom case
        if(ball.getShape().getGlobalBounds().top > 1080){
            lives--;

            ball = Ball(1920 / 2 - 10, 0);

            float x = (rand() % 200 - 100);
            if(x == 0) x = 50;
            float y = 100.0f;

            ball.setDirection(x, y);
        }

        // HUD
        stringstream ss;
        ss << "Score = " << score << "   Lives = " << lives;
        hud.setString(ss.str());

        // DRAW
        window.clear();
        window.draw(hud);
        window.draw(bat.getShape());
        window.draw(ball.getShape());
        window.display();
    }

    return 0;
}

#pragma once
#include <SFML/Graphics.hpp>
#include <cmath>

using namespace sf;

class Ball{
    private:
        Vector2f m_position;
        CircleShape m_shape;
        float m_speed = 600.0f;
        float m_directionX = 0.0f;
        float m_directionY = 0.0f;
    public:
        Ball(float startX, float startY){
            m_position.x = startX;
            m_position.y = startY;
            m_shape.setRadius(10);
            m_shape.setPosition(m_position);
            m_shape.setFillColor(Color::Blue);
        }

        CircleShape getShape(){
            return m_shape;
        }

        void update(Time dt){
            m_position.x += m_directionX * m_speed * dt.asSeconds();
            m_position.y += m_directionY * m_speed * dt.asSeconds();
            m_shape.setPosition(m_position);
        }

        void reboundSides(){
            m_directionX = -m_directionX;
        }

        void reboundTopBottom(){
            m_directionY = -m_directionY;
        }

	    void setPosition(float x, float y){
        	m_position.x = x;
        	m_position.y = y;
        	m_shape.setPosition(m_position);
	    }

        void setDirection(float x, float y){
        	float length = std::sqrt(x * x + y * y);
        	if(length != 0){
                m_directionX = x / length;
                m_directionY = y / length;
            }
        }
};


#pragma once
#include <SFML/Graphics.hpp>

using namespace sf;

class Bat{
    private:
        Vector2f m_position;
        RectangleShape m_shape;
        float m_speed = 1000.0f;
        bool m_movingLeft = false;
        bool m_movingRight = false;

    public:
        Bat(float startX, float startY){
            m_position.x = startX;
            m_position.y = startY;
            m_shape.setSize(Vector2f(400, 5));
            m_shape.setPosition(m_position);
        }

        RectangleShape getShape(){
            return m_shape;
        }

        void moveLeft(){
            m_movingLeft = true;
        }

        void moveRight(){
            m_movingRight = true;
        }

        void stopLeft(){
            m_movingLeft = false;
        }

        void stopRight(){
            m_movingRight = false;
        }

        void update(Time dt){
            // Moving the bat left nd right
            if(m_movingLeft){
                m_position.x -= m_speed * dt.asSeconds();
            }
            if(m_movingRight){
                m_position.x += m_speed * dt.asSeconds();
            }

            // Keeping the bat within the bounds of the window
            if(m_position.x < 0){
                m_position.x = 0;
            }
    		if(m_position.x > 1920 - m_shape.getSize().x){
                m_position.x = 1920 - m_shape.getSize().x;
            }
            m_shape.setPosition(m_position);
        }
};


// Zombie

#include <SFML/Graphics.hpp>
#include <sstream>
#include <iostream>
#include "player.h"
#include "zombie.h"
#include "bullet.h"
using namespace sf;
using namespace std;

int createBackground(VertexArray &rVA, IntRect arena);
Zombie *createHorde(int numZombies, IntRect arena);

int main(){
	// *** Setup (Declaration & Initialisation) ***
	VideoMode vm(1920, 1080);
	RenderWindow window(vm,"Zombie Shooter", Style::Fullscreen);

	View mainView(FloatRect(0, 0, 1920, 1080));
	View hudView(FloatRect(0, 0, 1920, 1080));

	enum class State{GAME_OVER, LEVELING_UP, PLAYING, PAUSED};

	State state = State::GAME_OVER;
    IntRect arena;
    Vector2f resolution;
    resolution.x = 1920;
    resolution.y = 1080;

	RectangleShape bar;
	bar.setSize(Vector2f(500, 500));
	bar.setPosition(0, 0);
	bar.setFillColor(Color::Red);

	Vector2f mouseWorldPosition; // relation to world coordinates
	Vector2i mouseScreenPosition; // relation to screen coordinates

	Texture textureBackground;
	textureBackground.loadFromFile("background_sheet.png");

	Texture textureGameOver;
	textureGameOver.loadFromFile("background.png");
	Sprite spriteGameOver;
	spriteGameOver.setTexture(textureGameOver);
	spriteGameOver.setPosition(0, 0);

	VertexArray background;

	window.setMouseCursorVisible(false);

	Texture textureCrosshair;
	textureCrosshair.loadFromFile("crosshair.png");

	Sprite spriteCrosshair;
	spriteCrosshair.setTexture(textureCrosshair);
	spriteCrosshair.setOrigin(25, 25);

	Font font;
    font.loadFromFile("zombiecontrol.ttf");

    //Paused Text
    Text pausedText;
    pausedText.setFont(font);
    pausedText.setString("Press Enter \nto Continue");
    pausedText.setCharacterSize(155);
    pausedText.setFillColor(Color::White);
	pausedText.setPosition(400, 400);

    //Game Over Text
    Text gameOverText;
    gameOverText.setFont(font);
    gameOverText.setString("Press Enter to Play");
    gameOverText.setCharacterSize(125);
    gameOverText.setFillColor(Color::White);

	FloatRect textRect = gameOverText.getLocalBounds();
	gameOverText.setOrigin(textRect.left + textRect.width / 2.0f, textRect.top + textRect.height / 2.0f);
	gameOverText.setPosition(1960 / 2.0f, 1080 / 2.0f);

	// Levelling Up
    Text levelUpText;
    levelUpText.setFont(font);
    levelUpText.setCharacterSize(80);
    levelUpText.setFillColor(Color::White);
	levelUpText.setPosition(150, 250);

	stringstream levelUpStream;
	levelUpStream <<
		"1- Increase rate of fire" <<
		"\n2- Increase clip size (next reload)" <<
		"\n3- Increase max health";

	levelUpText.setString(levelUpStream.str());

	// Score
	Text scoreText;
    scoreText.setFont(font);
    scoreText.setCharacterSize(55);
    scoreText.setFillColor(Color::White);
	scoreText.setPosition(20, 20);

	int score = 0;
	stringstream s;
	s << "Score: " << score;
	scoreText.setString(s.str());

	// High Score
	Text hiScoreText;
    hiScoreText.setFont(font);
    hiScoreText.setCharacterSize(55);
    hiScoreText.setFillColor(Color::White);
	hiScoreText.setPosition(1400, 0);

	int hiScore = 0;
	stringstream hs;
	hs << "High Score: " << hiScore;
	hiScoreText.setString(hs.str());

	// Zombies Remaining
    Text zombiesRemainingText;
    zombiesRemainingText.setFont(font);
    zombiesRemainingText.setString("Zombies: 100");
    zombiesRemainingText.setCharacterSize(55);
    zombiesRemainingText.setFillColor(Color::White);
	zombiesRemainingText.setPosition(1500, 980);

	// Zombies Remaining
    Text waveNumberText;
    waveNumberText.setFont(font);
    waveNumberText.setString("Wave: 0");
    waveNumberText.setCharacterSize(55);
    waveNumberText.setFillColor(Color::White);
	waveNumberText.setPosition(1250, 980);

	// Health Bar
	RectangleShape healthBar;
	healthBar.setFillColor(Color::Red);
	healthBar.setPosition(450, 980);
	healthBar.setSize(Vector2f(300, 70));

	// Create an Instance of Player
	Player player;

	int numZombies;
	int numZombiesAlive;
	Zombie *zombies = nullptr;

	int waves = 1;

	Bullet bullets[100];
	int currentBullet = 0;
	int bulletsSpare = 24;
	int bulletsInClip = 6;
	int clipSize = 6;
	float fireRate = 1;

	Time gameTimeTotal;
	Time lastPressed;

    Clock clock;

	// Game Loop
	while(window.isOpen()){
		// ------------ Event Handling Loop ------------
		Event event;
		while(window.pollEvent(event)){							// Event handle
			if(event.type == Event::Closed){
				window.close();
			}

			if(event.type == Event::KeyPressed){
				if(event.key.code == Keyboard::Return && state == State::GAME_OVER){
					state = State::LEVELING_UP;
				}

				else if(event.key.code == Keyboard::Return && state == State::PLAYING){
					state = State::PAUSED;
				}

				else if(event.key.code == Keyboard::Return && state == State::PAUSED){
					state = State::PLAYING;
				}
			}
		}
		// --------- End of Event Handling Loop ---------

		// -------------- To Quit the Game --------------
		if(Keyboard::isKeyPressed(Keyboard::Escape)){ 			// Keyboard handle (Escape Key)
			window.close();
		}

		// -------- Handle W A S D keys while playing --------
		if(state == State::PLAYING){
			if(Keyboard::isKeyPressed(Keyboard::W)){
				player.moveUp();
			}else{
				player.stopUp();
			}

			if(Keyboard::isKeyPressed(Keyboard::A)){
				player.moveLeft();
			}else{
				player.stopLeft();
			}

			if(Keyboard::isKeyPressed(Keyboard::S)){
				player.moveDown();
			}else{
				player.stopDown();
			}

		    if(Keyboard::isKeyPressed(Keyboard::D)){
				player.moveRight();
			}else{
				player.stopRight();
			}
			// --------------------------- Fire a Bullet ---------------------------
			if(Mouse::isButtonPressed(Mouse::Left)){
				if(gameTimeTotal.asMilliseconds() - lastPressed.asMilliseconds() > 1000 / fireRate){
					bullets[currentBullet].shoot(
						player.getCenter().x, // startX
						player.getCenter().y, // startY
						mouseWorldPosition.x, // targetX
						mouseWorldPosition.y  // targetY
					);

					currentBullet++;
					if(currentBullet > 99){
						currentBullet = 0;
					}
					lastPressed = gameTimeTotal;
				}
			}
		}

		// -------- Handle the LEVELING up state --------
		if(state == State::LEVELING_UP){
			if(event.key.code == Keyboard::Num1){
				state = State::PLAYING;
			}

			if(event.key.code == Keyboard::Num2){
				state = State::PLAYING;
			}

			if(event.key.code == Keyboard::Num3){
				state = State::PLAYING;
			}

			if(state == State::PLAYING){
				arena.width = 500 * waves;
            	arena.height = 500 * waves;
            	arena.left = 0;
            	arena.top = 0;
            	int tileSize = 50;

               	createBackground(background, arena);

            	// Spawn the player
            	player.spawn(arena, resolution, tileSize);

            	numZombies = 10;
            	numZombiesAlive = 10;
            	zombies = createHorde(numZombies, arena);

            	clock.restart();
			}
		}// ------------- End of LEVELING up -------------

		// ----------------- Update Part ----------------
		if(state == State::PLAYING){
			Time dt = clock.restart();
			float dtAsSeconds = dt.asSeconds();
			mouseScreenPosition = Mouse::getPosition();

			// Update total game time
			gameTimeTotal += dt;

			//Convert mouse position to world coordinates of mainView
			mouseWorldPosition = window.mapPixelToCoords(Mouse::getPosition(), mainView);

			spriteCrosshair.setPosition(mouseWorldPosition);

			// Update Player
			player.update(dtAsSeconds, Mouse::getPosition());

			// Update Zombies
			Vector2f playerLocation(player.getCenter());
			for(int i = 0; i < numZombies; i++){
				if(zombies[i].isAlive()){
					zombies[i].update(dtAsSeconds, playerLocation);
				}
			}

			// Update any bullets that are InFlight
			for(int i=0; i<100; i++){
				if(bullets[i].isInFlight()){
					bullets[i].update(dtAsSeconds);
				}
			}
			// Collision between bullets and zombies
			for(int i=0; i<100; i++){
				for(int j=0; j<numZombies; j++){
					if(bullets[i].isInFlight() && zombies[j].isAlive()){
						if(bullets[i].getPosition().intersects(zombies[j].getPosition())){
							// Stop the bullet
							bullets[i].stop();

							if(zombies[j].hit()){
								score += 10;
								if(score >= hiScore){
									hiScore = score;
								}
								numZombiesAlive--;
								// When all zombies are dead
								if(numZombiesAlive == 0){
									state = State::LEVELING_UP;
								}
							}
						}
					}
				}
			} // End of zombie and bullet collision

			// Update Score HUD
			// Update the score text
			s.str("");
			s << "Score: " << score;
			scoreText.setString(s.str());

			// Update the high score text
			hs.str("");
			hs << "High Score: " << hiScore;
			hiScoreText.setString(hs.str());

			mainView.setCenter(player.getCenter());
		}
		// -------------- End of Update Part -------------


		// -------------- Draw the Scene --------------
		window.clear();
		if(state == State::PLAYING){
			window.setView(mainView);
			window.draw(background, &textureBackground);
			window.draw(player.getSprite());

			for(int i = 0; i < numZombies; i++){
				window.draw(zombies[i].getSprite());
			}

			for(int i=0; i<100; i++){
				if(bullets[i].isInFlight()){
					window.draw(bullets[i].getShape());
				}
			}

			window.draw(spriteCrosshair);
			window.setView(hudView);
			window.draw(healthBar);
			window.draw(scoreText);
			window.draw(hiScoreText);
			window.draw(zombiesRemainingText);
			window.draw(waveNumberText);
		}

		if(state == State::LEVELING_UP){
			window.draw(levelUpText);
		}

		if(state == State::PAUSED){
			window.draw(pausedText);
		}

		if(state == State::GAME_OVER){
			window.draw(spriteGameOver);
			window.draw(gameOverText);
			window.draw(scoreText);
			window.draw(hiScoreText);
		}
		window.display();

	} // End of Game Loop

	return 0;
}

// Function to create scrolling background decoration
int createBackground(VertexArray &rVA, IntRect arena){
	const int TILE_SIZE = 50;
	const int TILE_TYPES = 3;
	const int VERTS_IN_QUAD = 4;

	rVA.setPrimitiveType(Quads);
	int worldWidth = arena.width/TILE_SIZE;
	int worldHeight = arena.height/TILE_SIZE;
	rVA.resize(worldWidth * worldHeight * VERTS_IN_QUAD);

	int currentVertex = 0;
	for (int w = 0; w < worldWidth; w++){ // Columns of the map
		for (int h = 0; h < worldHeight; h++){ // Rows of the map
			// Set the positions of 1 corner tile (top-left, top-right, bottom-right, bottom-left) of the entire arena
			rVA[currentVertex + 0].position = Vector2f(w * TILE_SIZE, h * TILE_SIZE);
			rVA[currentVertex + 1].position = Vector2f(w * TILE_SIZE + TILE_SIZE, h * TILE_SIZE);
			rVA[currentVertex + 2].position = Vector2f(w * TILE_SIZE + TILE_SIZE, h * TILE_SIZE + TILE_SIZE);
			rVA[currentVertex + 3].position = Vector2f(w * TILE_SIZE, h * TILE_SIZE + TILE_SIZE);

			// Filling Wall Tiles || Border check
			if(w == 0 || w == worldWidth-1 || h == 0 || h == worldHeight-1){
				rVA[currentVertex+0].texCoords = Vector2f(0, TILE_SIZE * TILE_TYPES);
				rVA[currentVertex+1].texCoords = Vector2f(TILE_SIZE, TILE_SIZE * TILE_TYPES);
				rVA[currentVertex+2].texCoords = Vector2f(TILE_SIZE, TILE_SIZE * TILE_TYPES + TILE_SIZE);
				rVA[currentVertex+3].texCoords = Vector2f(0, TILE_SIZE * TILE_TYPES + TILE_SIZE);
			}else{ // Rest of the random flooring of the arena
				srand((int)time(0)+ h * w - h);
				int mOrG = (rand() % TILE_TYPES);
				int verticalOffset = mOrG * TILE_SIZE;
				rVA[currentVertex+0].texCoords = Vector2f(0, verticalOffset);
				rVA[currentVertex+1].texCoords = Vector2f(TILE_SIZE, verticalOffset);
				rVA[currentVertex+2].texCoords = Vector2f(TILE_SIZE, TILE_SIZE + verticalOffset);
				rVA[currentVertex+3].texCoords = Vector2f(0, TILE_SIZE + verticalOffset);
			}
			currentVertex = currentVertex + VERTS_IN_QUAD;
		} // h loop end
	} // w loop end
	return TILE_SIZE;
} //function end

Zombie *createHorde(int numZombies, IntRect arena){

	Zombie *zombies = new Zombie[numZombies];

	int minX = arena.left + 25;
	int maxX = arena.width - 25;
	int minY = arena.top + 25;
	int maxY = arena.height - 25;

	for (int i = 0; i < numZombies; i++){
		// Which side should the zombie spawn
		srand((int)time(0) * i);
		int side = (rand() % 4);
		float x, y;

		switch(side){
			case 0:  // left
				x = minX;
				y = (rand() % maxY) + minY;
				break;
			case 1:  // right
				x = maxX;
				y = (rand() % maxY) + minY;
				break;
			case 2:  // top
				x = (rand() % maxX) + minX;
				y = minY;
				break;
			case 3:  // bottom
				x = (rand() % maxX) + minX;
				y = maxY;
				break;
		}
		// Select the type of Zombie (Bloater, chaser, or crawler)
		srand((int)time(0) * i * 2);
		int type = (rand() % 3);

		//Spawn the Zombie
		zombies[i].spawn(x, y, type, i);

	} // loop end

	return zombies;
} // function end

#include <SFML/Graphics.hpp>
#include <cmath>
using namespace sf;

class Bullet{
	private:
		Vector2f m_Position;
		RectangleShape m_BulletShape;
		bool m_InFlight = false;
		float m_BulletSpeed = 1000;
		float m_BulletSpeedX;
		float m_BulletSpeedY;

		// Boundaries so the bullet doesn't fly forever
		float m_MaxX;
		float m_MinX;
		float m_MaxY;
		float m_MinY;
	public:
		Bullet();
		void stop();
		bool isInFlight();
		FloatRect getPosition();
		RectangleShape getShape();

		void shoot(float startX, float startY, float targetX, float targetY);
		void update(float elapsedTime);
};

Bullet::Bullet(){
	m_BulletShape.setSize(Vector2f(5, 5));
	m_BulletShape.setFillColor(Color::Yellow);
}

void Bullet::stop(){
	m_InFlight = false;
}

bool Bullet::isInFlight(){
	return m_InFlight;
}

FloatRect Bullet::getPosition(){
	return m_BulletShape.getGlobalBounds();
}

RectangleShape Bullet::getShape(){
	return m_BulletShape;
}

void Bullet::shoot(float startX, float startY, float targetX, float targetY){
	m_InFlight = true;
	m_Position.x = startX;
	m_Position.y = startY;

	// Gradient approach
	float gradient = (targetY - startY) / (targetX - startX);
	if(gradient < 0){
		gradient = gradient*-1;
	}

	m_BulletSpeedX = m_BulletSpeed * (1.0/(1 + gradient));
	m_BulletSpeedY = m_BulletSpeedX * gradient;

	// Fix the directions
	if(targetX < startX){
		m_BulletSpeedX *= -1;
	}
	if(targetY < startY){
		m_BulletSpeedY *= -1;
	}

	// Set a max range of 1000 pixels
	float range = 1000;
	m_MinX = startX - range;
	m_MaxX = startX + range;
	m_MinY = startY - range;
	m_MaxY = startY + range;

	m_BulletShape.setPosition(m_Position);
}

void Bullet::update(float elapsedTime){
	// Update the bullet position variables
	m_Position.x += m_BulletSpeedX * elapsedTime;
	m_Position.y += m_BulletSpeedY * elapsedTime;

	// Move the bullet
	m_BulletShape.setPosition(m_Position);

	// Has the bullet gone out of range?
	if(m_Position.x < m_MinX || m_Position.x > m_MaxX || m_Position.y < m_MinY || m_Position.y > m_MaxY){
		m_InFlight = false;
	}
}


#include <SFML/Graphics.hpp>
#include <iostream>
#include <cmath>
using namespace sf;
using namespace std;

class Player{
	private:
		const float START_SPEED = 200;
		Vector2f m_Position;
		Texture m_Texture;
		Sprite m_Sprite;

		Vector2f m_Resolution;
		IntRect m_Arena; // Size of Current Arena
		int m_TileSize;

		bool m_LeftPressed;
		bool m_RightPressed;
		bool m_UpPressed;
		bool m_DownPressed;

		float m_Speed;

	public:
		Player();
		Sprite getSprite();
		FloatRect getPosition();
		Vector2f getCenter();

		void spawn(IntRect arena, Vector2f resolution, int tileSize);
		void update(float elapsedTime, Vector2i mouseScreenPosition);

		void moveLeft();
		void moveRight();
		void moveUp();
		void moveDown();

		void stopLeft();
		void stopRight();
		void stopUp();
		void stopDown();

};

Player::Player(){
	m_Speed = START_SPEED;
	m_Texture.loadFromFile("player.png");
	m_Sprite.setTexture(m_Texture);

	m_Sprite.setOrigin(25, 25);
	//m_Sprite.setPosition(1920/2.0f, 1080/2.0f);
	m_Position = m_Sprite.getPosition(); // keep updated
}

Sprite Player::getSprite(){
	return m_Sprite;
}

FloatRect Player::getPosition(){
	return m_Sprite.getGlobalBounds();
}

Vector2f Player::getCenter(){
	return m_Position;
}

void Player::moveLeft(){
	m_LeftPressed = true;
}

void Player::moveRight(){
	m_RightPressed = true;
}

void Player::moveUp(){
	m_UpPressed = true;
}

void Player::moveDown(){
	m_DownPressed = true;
}

void Player::stopLeft(){
	m_LeftPressed = false;
}

void Player::stopRight(){
	m_RightPressed = false;
}

void Player::stopUp(){
	m_UpPressed = false;
}

void Player::stopDown(){
	m_DownPressed = false;
}

void Player::spawn(IntRect arena, Vector2f resolution, int tileSize){
	// Place the player in the middle of the arena
	m_Position.x = arena.width / 2;
	m_Position.y = arena.height / 2;

	// Copy the details of the arena to the player's m_Arena
	m_Arena.left = arena.left;
	m_Arena.width = arena.width;
	m_Arena.top = arena.top;
	m_Arena.height = arena.height;

	// Remember how big the tiles are in this arena
	m_TileSize = tileSize;

	// Store the resolution for future use
	m_Resolution.x = resolution.x;
	m_Resolution.y = resolution.y;
}

void Player::update(float elapsedTime, Vector2i mouseScreenPosition){
	// Move the player from the current position to where the player moves
	if(m_UpPressed){
		m_Position.y -= m_Speed * elapsedTime;
	}
	if(m_DownPressed){
		m_Position.y += m_Speed * elapsedTime;
	}
	if(m_RightPressed){
		m_Position.x +=  m_Speed * elapsedTime;
	}
	if(m_LeftPressed){
		m_Position.x -=  m_Speed * elapsedTime;
	}

	m_Sprite.setPosition(m_Position);

	// Keep the player inside the arena
	if(m_Position.x > m_Arena.width - m_TileSize){
		m_Position.x = m_Arena.width - m_TileSize;
	}
	if(m_Position.x < m_Arena.left + m_TileSize){
		m_Position.x = m_Arena.left + m_TileSize;
	}
	if(m_Position.y < m_Arena.top + m_TileSize){
		m_Position.y = m_Arena.top + m_TileSize;
	}
	if(m_Position.y > m_Arena.height - m_TileSize){
		m_Position.y = m_Arena.height - m_TileSize;
	}

	// Calculate the angle the player is facing and rotate it to the direction the cursor is currently facing
	float angle;
	// Calculate the difference betweem x and y position of the cursor position to the player present at the center of the arena (dx,dy)
	float dx = mouseScreenPosition.x - m_Resolution.x/2;
	float dy = mouseScreenPosition.y - m_Resolution.y/2;
	// Use the formula of atan2(dx,dy) -> this gives the result in radians
	// Convert the angle in radians to degrees using the formula -> "rad*(180/pi)""
	angle = (atan2(dy,dx)*180)/3.141;

	// Set the rotation and NOT the position of the player
	m_Sprite.setRotation(angle);
}

#include <SFML/Graphics.hpp>
#include <cmath>
using namespace sf;

class Zombie{
	private:
		const float BLOATER_SPEED = 12;
		const float CHASER_SPEED = 14;
		const float CRAWLER_SPEED = 11;

		const float BLOATER_HEALTH = 5;
		const float CHASER_HEALTH = 1;
		const float CRAWLER_HEALTH = 3;

		Vector2f m_Position;
		Texture m_Texture;
		Sprite m_Sprite;

		float m_Speed;
		float m_Health;
		bool m_Alive = false;
	public:
		FloatRect getPosition();
		Sprite getSprite();
		bool isAlive();
		void spawn(float startX, float startY, int type, int seed);
		void update(float elapsedTime, Vector2f playerLocation);
		bool hit();
};

FloatRect Zombie::getPosition(){
	return m_Sprite.getGlobalBounds();
}

Sprite Zombie::getSprite(){
	return m_Sprite;
}

bool Zombie::isAlive(){
	return m_Alive;
}

void Zombie::spawn(float startX, float startY, int type, int seed){
	switch(type){
		case 0:
			m_Texture.loadFromFile("bloater.png");
			m_Sprite.setTexture(m_Texture);
			m_Speed = BLOATER_SPEED;
			m_Health = BLOATER_HEALTH;
			m_Sprite.setOrigin(25, 25);
			break;
		case 1:
			m_Texture.loadFromFile("chaser.png");
			m_Sprite.setTexture(m_Texture);
			m_Speed = CHASER_SPEED;
			m_Health = CHASER_HEALTH;
			m_Sprite.setOrigin(25, 25);
			break;
		case 2:
			m_Texture.loadFromFile("crawler.png");
			m_Sprite.setTexture(m_Texture);
			m_Speed = CRAWLER_SPEED;
			m_Health = CRAWLER_HEALTH;
			m_Sprite.setOrigin(25, 25);
			break;
	}

	m_Position.x = startX;
	m_Position.y = startY;

	m_Sprite.setPosition(m_Position);

	srand((int)time(0)*seed);
	float modifier = (rand() % (101-70)+70);
	modifier = modifier/100;
	m_Speed = m_Speed * modifier;
	m_Alive = true;
}

void Zombie::update(float elapsedTime, Vector2f playerLocation){
	float playerX = playerLocation.x;
	float playerY = playerLocation.y;

	// Update the zombie position based on player position
	if(m_Position.x < playerX){
		m_Position.x += m_Speed * elapsedTime;
	}
	if(m_Position.x > playerX){
		m_Position.x -= m_Speed * elapsedTime;
	}
	if(m_Position.y < playerY){
		m_Position.y += m_Speed * elapsedTime;
	}
	if(m_Position.y > playerY){
		m_Position.y -= m_Speed * elapsedTime;
	}

	m_Sprite.setPosition(m_Position);

	float angle;
	float dx = playerX - m_Position.x/2;

	float dy = playerY - m_Position.y/2;
	angle = (atan2(dy,dx)*180)/3.141;
	m_Sprite.setRotation(angle);
}

bool Zombie::hit(){
	m_Health--;
	if(m_Health <= 0){
		m_Alive = false;
		m_Texture.loadFromFile("blood.png");
		m_Sprite.setTexture(m_Texture);
		return true;
	}
	return false;
}
