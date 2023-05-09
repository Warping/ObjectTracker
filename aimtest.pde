static final float FRAMERATE = 30;
static final float SCALE = 7;

float turX = 50;
float turY = 80;
float projSpeed = 60; // meters / s
float targSpeed = 20;
float angleSpeed = 60; //degrees / sec
float initialDist = 10; //starting distance from tur

Turret tur;
Turret tur2;
ArrayList<Projectile> projs;
Projectile target;
boolean cooldown = false;

PVector projVel;
PVector targVel;

void setup() {
  frameRate(FRAMERATE);
  size(1000, 800);
  tur = new Turret(new PVector(turX / SCALE, turY / SCALE), angleSpeed, projSpeed, 1000);
  tur2 = new Turret(new PVector(turX / SCALE, turY / SCALE), angleSpeed, projSpeed, 1000);
  tur2.smartAim = false;
  projs = new ArrayList<Projectile>();
  target = new Projectile(new PVector(turX / SCALE, turY / SCALE + initialDist), targSpeed, 0, 5 / SCALE, color(0, 125, 255, 200));
}

void draw() {
  background(0);
  scale(SCALE);
  stroke(255);
  strokeWeight(2);
  textSize(30);
  PVector mouseTarg = new PVector(mouseX/ SCALE, mouseY / SCALE);
  //target.pos = mouseTarg;
  //tur.setTarget(mouseTarg);
  tur.setTarget(target.pos);
  tur.aimAt();
  //tur2.setTarget(mouseTarg);
  tur2.setTarget(target.pos);
  tur2.aimAt();
  if (tur.canFire() && tur.pred.shouldFire) {
    projs.add(new Projectile(tur.turPos, tur.projSpeed, tur.angle, 4 / SCALE, color(0, 255, 0, 100)));
  }
  if (tur2.canFire()) {
    projs.add(new Projectile(tur2.turPos, tur2.projSpeed, tur2.angle, 4 / SCALE, color(0, 125, 255, 100)));
  }
  float maxDist = 200;
  PVector closestProj = new PVector(0, 0);
  for (int i = projs.size() - 1; i >= 0; i--) {
    Projectile proj = projs.get(i);
    if (proj.getDist(tur.turPos) > 1000) {
      projs.remove(i);
      continue;
    }
    proj.update();
    proj.show();
    if (target.getDist(proj.pos) < maxDist) {
      closestProj = proj.pos.copy();
      maxDist = target.getDist(proj.pos);
    }
  }
  //if (frameCount % 5 == 0) target.setAngle(target.vel.heading() + map(noise(frameCount / 10.0), 0, 1, -0.2, 0.2));
  //target.update();
  //target.setAngle(tur.targetPos.heading() - PI / 2);
  target.update(new PVector(-3, -7).mult(1.0 / frameRate));
  target.show();
  tur.show();
  tur2.show();
  strokeWeight(2 / SCALE);
  line(target.pos.x, target.pos.y, closestProj.x, closestProj.y);
}
