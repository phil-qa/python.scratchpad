using System;
using System.Linq;
using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;



class Player
{
	static void Main(string[] args)
	{
            string[] inputs;
            List<Checkpoint> checkpoints = new List<Checkpoint>();
            var checkpointId = 1;
            var courseIsKnown = false;
            var action = "";
            var thrust = 100;
            var previousCheckpoint = new Checkpoint() { Id = 0 };
            var nextCheckpoint = new Checkpoint();
            var distanceRecord = 0;
            Race race = new Race();
		// game loop
		while (true)
		{
                inputs = Console.ReadLine().Split(' ');
                int x = int.Parse(inputs[0]);
                int y = int.Parse(inputs[1]);
                int nextCheckpointX = int.Parse(inputs[2]); // x position of the next check point
                int nextCheckpointY = int.Parse(inputs[3]); // y position of the next check point
                int nextCheckpointDist = int.Parse(inputs[4]); // distance to the next checkpoint
                int nextCheckpointAngle = int.Parse(inputs[5]); // angle between your pod orientation and the direction of the next checkpoint
                inputs = Console.ReadLine().Split(' ');
                int opponentX = int.Parse(inputs[0]);
                int opponentY = int.Parse(inputs[1]);

                // Write an action using Console.WriteLine()
                // To debug: Console.Error.WriteLine("Debug messages...");


                var approachingPoint = new Checkpoint() { CheckpointX = nextCheckpointX, CheckpointY = nextCheckpointY, NextCheckpointDistance = nextCheckpointDist };
                race.ParseToCheckPoint(nextCheckpointX, nextCheckpointY);
                if(!race.CourseIsKnown)
                    race.MyRacer.Update(nextCheckpointX,nextCheckpointY);
                    else
                    race.MyRacer.Update(nextCheckpointAngle, nextCheckpointX, nextCheckpointY, x, y, nextCheckpointDist);
			    log($"checkpoit:{race.MyRacer.ActiveCheckpoint}, brakePoint {race.MyRacer.BrakePoint}, Speed {race.MyRacer.Speed}");
				Console.WriteLine(race.MyRacer.ToString());
		}
	}


	private static void log(string message)
	{
		Console.Error.WriteLine($"{message}");
	}


}

    public class Race
    {
        private int _numberOfCheckpoints = 0;
        public List<Checkpoint> Checkpoints;
        public Racer MyRacer;

        public bool CourseIsKnown { get; set; }

        public Race()
        {
            Checkpoints = new List<Checkpoint>();
            MyRacer = new Racer(1,1);
            CourseIsKnown = false;
        }

        public void ParseToCheckPoint(int nextCheckpointX, int nextCheckpointY)
        {
            _numberOfCheckpoints = Checkpoints.Count;
            var newCheckpoint = new Checkpoint(nextCheckpointX, nextCheckpointY);
            if (_numberOfCheckpoints == 0)

            {
                newCheckpoint.Id = 1;
                Checkpoints.Add(newCheckpoint);
            }
            else
             if (!Checkpoints.Any(cp => cp.NextCheckPointX == nextCheckpointX && cp.NextCheckpointY == nextCheckpointY))
            {
                newCheckpoint.Id = Checkpoints.Count() + 1;
                Checkpoints.Add(newCheckpoint);
            }
            else
            if (_numberOfCheckpoints > 1 && nextCheckpointX == Checkpoints.First().NextCheckPointX && nextCheckpointY == Checkpoints.First().NextCheckpointY)
                if (!CourseIsKnown)
                {
                    CourseIsKnown = true;
                    PopulateSourceCoordinates();
                    BuildCheckpointCharacteristics();
                    MyRacer.Checkpoints = Checkpoints;
                }
        }

        private void PopulateSourceCoordinates()
        {
            foreach (var point in Checkpoints)
            {
                var previousPoint = GetPreviosuCheckpoint(point.Id);
                point.SetVectors(previousPoint.NextCheckPointX, previousPoint.NextCheckpointY);
            }
        }

        private void BuildCheckpointCharacteristics()
        {
            foreach (var checkpoint in Checkpoints)
            {
                var sourcePoint = checkpoint;
                var previousPoint = GetPreviosuCheckpoint(sourcePoint.Id);
                var nextPoint = GetNextCheckpoint(checkpoint.Id);
                var followingPoint = GetNextCheckpoint(nextPoint.Id);



                sourcePoint.BuildCharacteristics(previousPoint, nextPoint, followingPoint);
            }
        }

        private Checkpoint GetNextCheckpoint(int id)
        {
            if (id + 1 > Checkpoints.Last().Id)
                return Checkpoints.First();
            else
                return Checkpoints.First(cp => cp.Id == id + 1);
        }

        private Checkpoint GetPreviosuCheckpoint(int id)
        {
            if (id == 1)
                return Checkpoints.Last();
            else
                return Checkpoints.First(cp => cp.Id == id - 1);
        }
    }

    public class Racer
    {
        public List<Checkpoint> Checkpoints;
        public int XPosition;
        public int YPosition;
        public int DistanceFromNextCheckpoint;
        public double AngleAToNextCheckpoint;
        public int Thrust { get; set; }
        public double BrakePoint { get; set; }
        public Checkpoint ActiveCheckpoint { get; set; }
        
        public double Speed { get; set; }
        public bool? PointPassed { get; set; }

        private int previousx;
        private int previousy;
        private Checkpoint previousCheckpoint;

        public Racer(int xPosition, int yPosition)
        {
            Checkpoints = new List<Checkpoint>();
            XPosition = xPosition;
            YPosition = yPosition;
            Thrust = 100;
        }

        public void Update(double angleToCheckpoint, int nextCheckpointX, int nextCheckpointY, int shipX, int shipY, int distanceToNextCheckpoint)
        {
            if (ActiveCheckpoint != null)
                previousCheckpoint = ActiveCheckpoint;
            ActiveCheckpoint = Checkpoints.First(cp => cp.NextCheckPointX == nextCheckpointX && cp.NextCheckpointY == nextCheckpointY);
            if (ActiveCheckpoint != previousCheckpoint)
                PointPassed = true;
            else
            {
                PointPassed = false;
            }
            previousx = XPosition;
            previousy = YPosition;
            XPosition = shipX;
            YPosition = shipY;
            Speed = Math.Sqrt(Math.Pow((XPosition - previousx), 2) + Math.Pow((YPosition - previousy), 2));
            AngleAToNextCheckpoint = angleToCheckpoint;
            DistanceFromNextCheckpoint = distanceToNextCheckpoint;
            BrakePoint = ActiveCheckpoint.MaximumBrakeDistance * (ActiveCheckpoint.OutsideAngle / 360);
            if (distanceToNextCheckpoint < BrakePoint)
                Thrust = (int)(100 - (100 * (ActiveCheckpoint.OutsideAngle / 360)));
            else
                Thrust = 100;
        }
        public void Update(int nextCheckpointX, int nextCheckpointY)
        {
            ActiveCheckpoint = new Checkpoint(nextCheckpointX, nextCheckpointY);
        }

        public override string ToString()
        {
            return ($"{ActiveCheckpoint.NextCheckPointX} {ActiveCheckpoint.NextCheckpointY} {Thrust}");
        }
        private static void log(string message)
        {
            Console.Error.WriteLine($"{message}");
        }

    }
    public class Checkpoint
    {
        public int Id;
        public int CheckpointX;
        public int CheckpointY;
        public int NextCheckPointX;
        public int NextCheckpointY;
        public double NextCheckpointDistance;
        public double connectionDistance;
        public double returningDistance;
        public double AngleAtPoint;
        public double OutsideAngle;
        public double MaximumBrakeDistance { get; set; }

        public Checkpoint(int nextCheckpointX, int nextCheckpointY)
        {
            NextCheckPointX = nextCheckpointX;
            NextCheckpointY = nextCheckpointY;
        }

        public Checkpoint()
        {

        }


        internal void BuildCharacteristics(Checkpoint PreviousPoint, Checkpoint nextPoint, Checkpoint followingPoint)
        {
            NextCheckpointDistance = Math.Sqrt((Math.Pow((CheckpointX - nextPoint.CheckpointX), 2) + Math.Pow((CheckpointY - nextPoint.CheckpointY), 2)));
            connectionDistance = Math.Sqrt((Math.Pow((NextCheckPointX - followingPoint.CheckpointX), 2) + Math.Pow((NextCheckpointY - followingPoint.CheckpointY), 2)));
            returningDistance = Math.Sqrt((Math.Pow((CheckpointX - followingPoint.CheckpointX), 2) + Math.Pow((CheckpointY - followingPoint.CheckpointY), 2)));
            var numerator = Math.Pow(NextCheckpointDistance, 2) + Math.Pow(connectionDistance, 2) - Math.Pow(returningDistance, 2);
            var denominator = 2 * NextCheckpointDistance * connectionDistance;
            AngleAtPoint = Math.Acos(numerator / denominator);
            AngleAtPoint = AngleAtPoint * (180.0 / Math.PI);
            OutsideAngle = 360 - AngleAtPoint;
            MaximumBrakeDistance = NextCheckpointDistance * .4;
        }

        internal void SetVectors(int nextCheckPointX, int nextChepointY)
        {
            CheckpointX = nextCheckPointX;
            CheckpointY = nextChepointY;
        }
    }
