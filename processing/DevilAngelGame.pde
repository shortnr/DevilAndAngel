int boardWidth = 10;
int boardHeight = 10;
int cellWidth = 40;
int cellHeight = 40;
int winWidth;
int winHeight;

int bomb_x = 9;
int bomb_y = 3;
int robot_x = 5;
int robot_y = 10;

PImage tempRobot;
PImage robot;
PImage bomb;

color red = color(255, 0, 0);
color blue = color(0, 0, 255);

float robotScale = (float)1/8;
float bombScale = 0.125;

void setup() {
  winWidth = cellWidth * (boardWidth + 2);
  winHeight = cellHeight * (boardHeight + 2);
  size(480, 480);
  tempRobot = loadImage("robot.png");
  robot = createImage(tempRobot.width, tempRobot.height, ARGB);
  
  for(int i = 0; i < tempRobot.width; i++)
  {
     for(int j = 0; j < tempRobot.height; j++)
     {
        int pixel = j * tempRobot.width + i;
        if(tempRobot.pixels[pixel] == color(255, 255, 255))
           robot.pixels[pixel] = color(255, 255, 255, 0);
        else
           robot.pixels[pixel] = tempRobot.pixels[pixel];
     }
  }
  
  PImage tempBomb = loadImage("bomb.png");
  bomb = createImage(tempBomb.width, tempBomb.height, ARGB);
  
  for(int i = 0; i < tempBomb.width; i++)
  {
     for(int j = 0; j < tempBomb.height; j++)
     {
        int pixel = j * tempBomb.width + i;
        if(tempBomb.pixels[pixel] == color(255, 255, 255))
           bomb.pixels[pixel] = color(255, 255, 255, 0);
        else
           bomb.pixels[pixel] = tempBomb.pixels[pixel];
     }
  }
  
  background(255);
  noLoop();
}

void draw() {
   for(int i = 0; i < boardWidth; i++)
   {
     for(int j = 0; j < boardHeight; j++)
     {
        int x = cellWidth * i + cellWidth;
        int y = cellHeight * j + cellHeight;
        
        rect(x, y, cellWidth, cellHeight); 
     }
   }
     
   bomb.resize((int)(bomb.width * bombScale), (int)(bomb.height * bombScale));
   image(bomb, bomb_x * cellWidth + 4, bomb_y * cellHeight + 4);
    
   robot.resize((int)(robot.width * robotScale), (int)(robot.height * robotScale));
   image(robot, robot_x * cellWidth + 6, robot_y * cellWidth + 5);
   
   drawArrow(red, 6, 9, 'd');
   drawArrow(blue, 6, 8, 'n');
   drawArrow(red, 7, 7, 'd');
   drawArrow(blue, 7, 6, 'n');
   drawArrow(red, 8, 5, 'd');
   drawArrow(blue, 8, 4, 'n');
    
   save("image.png");
}

void drawArrow(color c, int cellX, int cellY, char direction) {
    int x = cellWidth * cellX;
    int y = cellHeight * (cellY);
    
    strokeWeight(3);
    stroke(c);
    
    switch(direction) {
       case 'n':
          line(x + cellWidth / 2, y + cellHeight - 5, x + cellWidth / 2, y + 5);
          line(x + cellWidth / 2, y + 5, x + cellWidth / 2 - 7, y + 20);
          line(x + cellWidth / 2, y + 5, x + cellWidth / 2 + 7, y + 20);
          break;
       case 'e':
          line(x + 5, y + cellHeight / 2, x + cellWidth - 5, y + cellHeight / 2);
          line(x + cellWidth - 5, y + cellHeight / 2, x + cellWidth - 20, y + cellHeight / 2 + 7);
          line(x + cellWidth - 5, y + cellHeight / 2, x + cellWidth - 20, y + cellHeight / 2 - 7);
          break;
       case 'd':
          push();
          translate(x + cellWidth / 2, y + cellHeight / 2);
          rotate(PI / 4);
          translate(-19, -19);
          line(cellWidth / 2, cellHeight - 5, cellWidth / 2, 5);
          line(cellWidth / 2, 5, cellWidth / 2 - 7, 20);
          line(cellWidth / 2, 5, cellWidth / 2 + 7, 20);
          pop();
          break;
       default:
          break;
    }
}
