class Projectile {
  
  PVector pos;
  PVector vel;
  float size;
  color c;
  float maxSpeed = -1;
  
  Projectile(PVector _pos, float speed, float angle, float _size, color _c) {
    pos = _pos.copy();
    vel = PVector.fromAngle(angle);
    vel.setMag(speed);
    size = _size;
    c = _c;
  }
  
  Projectile(PVector _pos, float speed, float angle, float _size, color _c, float _maxSpeed) {
    pos = _pos.copy();
    vel = PVector.fromAngle(angle);
    vel.setMag(speed);
    size = _size;
    c = _c;
    maxSpeed = _maxSpeed;
  }
  
  void setVel(float speed, float angle) {
    vel = PVector.fromAngle(angle);
    vel.setMag(speed);
  }
  
  void setAngle(float angle) {
    float speed = vel.mag();
    vel = PVector.fromAngle(angle);
    vel.setMag(speed);
  }
  
  void update(PVector acc) {
    vel.add(acc);
    if (vel.mag() > maxSpeed && maxSpeed > 0) vel.setMag(maxSpeed);
    PVector _vel = vel.copy();
    _vel.mult(1.0 / frameRate);
    pos.add(_vel);
  }
  
  void update() {
    PVector _vel = vel.copy();
    _vel.mult(1.0 / frameRate);
    pos.add(_vel);
  }
  
  float getDist(PVector origin) {
    return dist(pos.x, pos.y, origin.x, origin.y);
  }
  
  void show() {
    push();
    fill(c);
    noStroke();
    circle(pos.x, pos.y, size);
    pop();
  }

}
