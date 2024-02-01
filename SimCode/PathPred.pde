import java.lang.Math.*;

class PathPred {

  ArrayList<PVector> pos;
  ArrayList<PVector> vel;
  ArrayList<PVector> acc;
  ArrayList<PVector> jrk;
  float t = 0;
  boolean shouldFire = false;
  ArrayList<Float> frameRates;
  PVector newPos;
  PVector prevPos;
  
  PolySolve solver = new PolySolve();
  
  PathPred(ArrayList<PVector> _pos, ArrayList<Float> _frameRates, int size) {
    pos = _pos;
    frameRates = _frameRates;
    vel = new ArrayList<>();
    acc = new ArrayList<>();
    jrk = new ArrayList<>();
    for (int i = 0; i < size; i++) {
      if (i > 0) vel.add(new PVector(0, 0));
      if (i > 1) acc.add(new PVector(0, 0));
      if (i > 2) jrk.add(new PVector(0, 0));
    }
  }
  
  void calcVals(PVector projVel) {
    for (int i = 0; i < pos.size() - 1; i++) {
      vel.set(i, pos.get(i + 1).copy().sub(pos.get(i)).mult(frameRates.get(i + 1)));
    }
    for (int i = 0; i < vel.size() - 1; i++) {
      acc.set(i, vel.get(i + 1).copy().sub(vel.get(i)).mult(frameRates.get(i + 1)));
    }
    for (int i = 0; i < acc.size() - 1; i++) {
      jrk.set(i, acc.get(i + 1).copy().sub(acc.get(i)).mult(frameRates.get(i + 1)));
    }
    PVector avgAcc = new PVector(0, 0);
    PVector avgJrk = new PVector(0, 0);
    for (int i = 0; i < pos.size(); i++) {
      if (i < acc.size()) avgAcc.add(acc.get(i));
      if (i < jrk.size()) avgJrk.add(jrk.get(i));
    }
    avgAcc.mult(1.0 / acc.size());
    avgJrk.mult(1.0 / jrk.size());
    PVector curPos = pos.get(pos.size() - 1);
    PVector curVel = vel.get(vel.size() - 1);
    //PVector curAcc = acc.get(acc.size() - 1);
    PVector curAcc = avgAcc.copy();
    if (avgJrk.mag() < 5) {
      float e = curPos.magSq();
      float d = 2 * curPos.dot(curVel);
      float c = curPos.dot(curAcc) + curVel.magSq() - projVel.magSq();
      float b = curVel.dot(curAcc);
      float a = 0.25 * curAcc.magSq();
      double[] tVals = solver.solveQuartic(a, b, c, d, e);
      if (tVals != null && tVals.length > 2) {
        t = (float) tVals[2];
        if (t < 2) {
          shouldFire = true;
          //println(tVals);
          newPos = curPos.copy().add(curVel.copy().mult(t));
          newPos.add(curAcc.mult(0.5 * t*t));
        }
      }
      //println(solver.solveQuartic(1, -7, 5, 31, -30));
    } else {
      shouldFire = false;
    }
    
  }
  
  void viewVals() {
    push();
    translate(0 + 100 / SCALE, 0 + 100 / SCALE);
    stroke(255);
    textSize(25 / SCALE);
    String curPos = "";
    String curVel = "";
    //String curAcc = "";
    //String curJrk = "";
    PVector avgAcc = new PVector(0, 0);
    PVector avgJrk = new PVector(0 ,0);
    for (int i = 0; i < pos.size(); i++) {
      curPos += pos.get(i) + " ";
      if (i < vel.size()) curVel += vel.get(i) + " ";
      if (i < acc.size()) avgAcc.add(acc.get(i));
      if (i < jrk.size()) avgJrk.add(jrk.get(i));
    }
    avgAcc.mult(1.0 / acc.size());
    avgJrk.mult(1.0 / jrk.size());
    if (shouldFire) text("Good to calc!", 0, 4*40 / SCALE);
    text(curPos, 0, 0*40 / SCALE);
    text(curVel, 0, 1*40 / SCALE);
    text(avgAcc.toString(), 0, 2*40 / SCALE);
    text(avgJrk.toString(), 0, 3*40 / SCALE);
    
    pop();
  }

}
