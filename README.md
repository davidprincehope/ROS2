# 🐢 Turtle Extermination Fun with ROS2

Ever wondered what happens when `turtle1` goes on a mission to catch all other turtles? 🐢💨  
This project makes it happen in **ROS2** with some PID magic!

---

## What’s Inside

- **TurtleSpawnerNode** – Spawns turtles at random spots with random orientations. 🎲  
- **TurtleControllerNode** – Makes `turtle1` chase and “excommunicate” the other turtles using **PID control**. 🚀  

---

## How to Play

1. Start the turtlesim:

```bash
ros2 run turtlesim turtlesim_node
````

2. Spawn the turtles:

```bash
ros2 run <your_package> turtle_spawner
```

3. Let `turtle1` do its thing:

```bash
ros2 run <your_package> turtle_controller
```

Watch `turtle1` go full ninja on the other turtles! 🥷🐢

---

## Fun Features

* Random turtle spawning
* Real-time tracking of `turtle1`
* Smooth PID-controlled movement
* Automatic turtle “excommunication” with logs 📝

---

## PID Magic ✨

* Keeps `turtle1` pointed in the right direction
* Adjusts speed so it doesn’t overshoot targets
* Tuned for fun and efficiency

---

## Custom Message: `NameOrientation.msg`

```text
string turtle_name
float64 random_x
float64 random_y
float64 random_theta
```

* `turtle_name` – Name of the spawned turtle
* `random_x`, `random_y` – Random position coordinates
* `random_theta` – Random orientation of the turtle

---

## License

MIT
