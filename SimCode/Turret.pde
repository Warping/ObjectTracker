
class Turret {
  
  PathPred pred;
  
  boolean smartAim;
  float roundsPerSec;
  float angle;
  float newAngle;
  float angleSpeed;
  float projSpeed;
  PVector turPos;
  PVector targetPos;
  PVector targetVel;
  PVector projVel;
  ArrayList<PVector> prevPos;
  ArrayList<Float> frameRates;
  final int PREV_POS_SIZE = floor(30);
  //final int PREV_POS_SIZE = 10;
  
  Turret(PVector pos, float _angleSpeed, float _projSpeed, int rpm) {
    roundsPerSec = rpm / 60.0;
    projSpeed = _projSpeed;
    turPos = pos;
    angle = 0;
    angleSpeed = radians(_angleSpeed);
    prevPos = new ArrayList<>();
    frameRates = new ArrayList<>();
    pred = new PathPred(prevPos, frameRates, PREV_POS_SIZE);
    smartAim = true;
  }
  
  void show() {
    push();
    translate(turPos.x, turPos.y);
    //text("Angle: " + degrees(angle), 0, 50);
    //text("New Angle: " + degrees(newAngle), 0, 100);
    //text("Delta Angle: " + round(degrees(newAngle - angle) * 100) / 100.0, 0, 150);
    //text("Vel: " + round(targetVel.mag()), 0, 200);
    noFill();
    stroke(255, 180);
    strokeWeight(4 / SCALE);
    beginShape();
    for (PVector p : prevPos) {
      //circle(p.x, p.y, 4 / SCALE);
      vertex(p.x, p.y);
    }
    endShape();
    circle(0, 0, 30 / SCALE);
    PVector barrel = PVector.fromAngle(angle);
    barrel.setMag(40 / SCALE);
    if (newAngle - angle == 0 && smartAim) stroke(0, 255, 0, 200);
    if (newAngle - angle == 0 && !smartAim) stroke(0, 0, 255, 200);
    line(0, 0, barrel.x, barrel.y);
    stroke(255, 0, 0, 120);
    line(0, 0, targetPos.x, targetPos.y);
    stroke(255, 0 ,255, 120);
    textSize(32 / SCALE);
    text("Dist: " + targetPos.mag(), 0, 100 / SCALE);
    stroke(255, 155, 0, 120);
    translate(targetPos.x, targetPos.y);
    line(0, 0, targetVel.x, targetVel.y);
    textSize(30);
    pop();
  }
  
  void rotateTo(float _newAngle) {
    newAngle = _newAngle;
    if (angleSpeed < 0) {
      angle = newAngle % TWO_PI;
      return;
    }
    if (abs(newAngle - angle) < angleSpeed / frameRate) {
      angle = newAngle;
    }
    if (angle > PI / 2 && newAngle < -PI / 2) {angle += (angleSpeed / frameRate);}
    else if (newAngle > PI / 2 && angle < -PI / 2) {angle -= (angleSpeed / frameRate);}
    else if (angle < newAngle) { angle += (angleSpeed / frameRate);}
    else if (angle > newAngle) {angle -= (angleSpeed / frameRate);}
    angle = angleFix(angle);
  }
  
  void setTarget(PVector _targPos) { //Data passed to this function is from the camera
    if(targetPos == null) {
      targetPos = _targPos.copy().sub(turPos);
      for (int i = 0; i < PREV_POS_SIZE; i++) {
        prevPos.add(targetPos);
        frameRates.add(frameRate);
      }
    }
    PVector targetOldPos = targetPos.copy();
    targetPos = _targPos.copy().sub(turPos);
    frameRates.remove(0);
    frameRates.add(frameRate);
    prevPos.remove(0);
    prevPos.add(targetPos);
    targetOldPos.sub(targetPos);
    //targetOldPos.mult(-1);
    targetOldPos.mult(-frameRate);
    targetVel = targetOldPos.copy();
  }
  
  PVector getVel() {
    return targetVel;
  }
  
  void aimAt() {
    //New Aim
    //angle = targetPos.heading();
    projVel = PVector.fromAngle(angle);
    projVel.setMag(projSpeed);
    if (frameCount > FRAMERATE) pred.calcVals(projVel);
    //pred.viewVals();
    //if (smartAim) {
      if (pred.shouldFire) {
        rotateTo(pred.newPos.heading());
      }
      else {
        rotateTo(targetPos.heading() + calcLeadAngle());
      }
    //} else {
    //  rotateTo(targetPos.heading() + calcLeadAngle());
    //}
    //Vel calc angle
    //PVector _targetPos = targetPos.copy();
    //_targetPos.sub(turPos);
    //projVel = PVector.fromAngle(angle);
    //projVel.setMag(projSpeed);
    //PVector newVec = projVel.copy();
    //newVec.add(targetVel);
    //if (SMART_AIM) {
    //  int sign = sign(newVec.heading() - projVel.heading());
    //  newAngle = sign * PVector.angleBetween(projVel, newVec);
    //  newAngle += _targetPos.heading();
    //  newAngle = angleFix(newAngle);
    //  rotateTo(newAngle);
    //  push();
    //  translate(turPos.x, turPos.y);
    //  line (0, 0, newVec.x, newVec.y);
    //  textSize(30);
    //  text("Angle extra: " + degrees(PVector.angleBetween(projVel, targetVel)), 0, 500);
    //  pop();
    //} else {
    //  newAngle = _targetPos.heading();
    //  rotateTo(_targetPos.heading());
    //}
  }
  
  boolean canFire() {
    return (newAngle - angle == 0);
  }
  
  float angleFix(float angle) {
    if (angle > PI) {
      angle = -PI + (angle - PI);      
    } else if (angle < -PI) {
      angle = PI - (angle + PI);
    }
    return angle;
  }
  
  int sign(float x) {
    return (x < 0) ? -1 : ((x == 0) ? 0 : 1);
  }
  
  float calcLeadAngle() {
    float alpha = PI - PVector.angleBetween(targetPos, targetVel);
    PVector newVec = targetPos.copy().add(targetVel);
    return sign(newVec.heading() - targetPos.heading()) * asin(sin(alpha) * targetVel.mag() / projVel.mag());
    
    //int sign = sign(newVec.heading() - projVel.heading());
    //newAngle = sign * PVector.angleBetween(projVel, newVec);
    //newAngle += _targetPos.heading();
    //newAngle = angleFix(newAngle);
    //text("Angle extra: " + degrees(deltaAngle), 0, 500);
  }

}
