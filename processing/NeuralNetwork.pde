int radius = 60;
int spacing;
int buffer = 2;
int input_layer_size = 3;
int hidden_layer_size = 4;
int output_layer_size = 2;
int largest_layer = 0;
int offset = 0;

color blue = color(100, 100, 255);
color black = color(0, 0, 0);
color light_gray = color(200, 200, 200);
color dark_gray = color(50, 50, 50);

Neuron[] input_layer;
Neuron[] hidden_layer;
Neuron[] output_layer;

void setup() {
   size(401, 401);
   input_layer = new Neuron[input_layer_size];
   hidden_layer = new Neuron[hidden_layer_size];
   output_layer = new Neuron[output_layer_size];
   if(input_layer_size > largest_layer)
      largest_layer = input_layer_size;
   if(hidden_layer_size > largest_layer)
      largest_layer = hidden_layer_size;
   if(output_layer_size > largest_layer)
      largest_layer = output_layer_size;
      
   spacing = (height - largest_layer * radius - 2 * buffer) / (largest_layer - 1);
   
   offset = (height - (input_layer_size * radius + spacing * (input_layer_size - 1))) / 2 + radius / 2;
   for(int i = 0; i < input_layer_size; i++)
      input_layer[i] = new Neuron('i', i + 1, radius / 2 + buffer, (radius + spacing) * i + offset, blue);
   
   offset = radius / 2 + buffer;
   for(int i = 0; i < hidden_layer_size; i++)
      hidden_layer[i] = new Neuron('h', i + 1, width / 2, (radius + spacing) * i + offset, blue);
      
   offset = (height - (output_layer_size * radius + spacing * (output_layer_size - 1))) / 2 + radius / 2;
   for(int i = 0; i < output_layer_size; i++)
      output_layer[i] = new Neuron('o', i + 1, width - radius / 2 - buffer, (radius + spacing) * i + offset, blue);
     
   println(str(hidden_layer[0].x - input_layer[0].x));
   println(str(input_layer[0].y - hidden_layer[0].y));
   noLoop();
}

void draw() {
   background(255);
   
   for(int i = 0; i < input_layer_size; i++) {
      input_layer[i].draw();
      input_layer[i].draw_connections(hidden_layer, light_gray);
   }
      
   for(int i = 0; i < hidden_layer_size; i++) {
      hidden_layer[i].draw();
      hidden_layer[i].draw_connections(output_layer, light_gray);
   }
   hidden_layer[0].draw_connections_reverse(input_layer, black);
      
   for(int i = 0; i < output_layer_size; i++)
      output_layer[i].draw();
      
   fill(black);
   textAlign(CENTER);
   textSize(18);
   text('w', 100, 50);
   text('w', 110, 90);
   text('w', 150, 125);
   textSize(12);
   text('1', 110, 55);
   text('2', 120, 95);
   text('3', 160, 130);
      
   save("image.png");
}

public class Neuron {
   public int number, x, y;
   public char layer;
   public color c;
   
   public Neuron(char _layer, int _number, int _x, int _y, color _c) {
      layer = _layer;
      number = _number;
      x = _x;
      y = _y;
      c = _c;
   }
   
   public void draw() {
      int text_offset = 5;
      fill(c);
      strokeWeight(2);
      circle(x, y, radius);
      fill(black);
      textAlign(CENTER);
      textSize(24);
      text(layer, x - text_offset, y + text_offset);
      textSize(18);
      text(str(number), x + textWidth(layer) + 4 - text_offset, y + 4 + text_offset);
   }
   
   public void draw_connections(Neuron[] layer, color c) {
      stroke(c);
      for(int i = 0; i < layer.length; i++) {
         line(x + radius / 2, y, layer[i].x - radius / 2, layer[i].y);
      }
      
      stroke(black);
   }
   
   public void draw_connections_reverse(Neuron[] layer, color c) {
      stroke(c);
      for(int i = 0; i < layer.length; i++) {
         line(x - radius / 2, y, layer[i].x + radius / 2, layer[i].y);
      }
      
      stroke(black);
   }
}
