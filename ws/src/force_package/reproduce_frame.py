
import numpy as np
from scipy.spatial.transform import Rotation as R

def calculate_orientation_vector(p1, p2):
    # Vector from P1 to P2
    v = np.array(p2) - np.array(p1)
    norm = np.linalg.norm(v)
    
    print(f"P1: {p1}")
    print(f"P2: {p2}")
    print(f"Vector P1->P2: {v}")
    print(f"Norm: {norm}")

    if norm < 1e-6:
        print("Points too close!")
        return None
    
    # Normalize Z-axis (force direction is now Z)
    z_axis = v / norm
    print(f"Z-axis (Force Direction): {z_axis}")
    
    # Create arbitrary X-axis
    world_z = np.array([0, 0, 1])
    
    # If Z is parallel to World Z, choose World X as temp X
    if np.abs(np.dot(z_axis, world_z)) > 0.99:
        print("Z is parallel to World Z, using World X as temp X")
        temp_x = np.array([1, 0, 0])
    else:
        # Cross World Z with our Z-axis to get a horizontal vector
        temp_x = np.cross(world_z, z_axis)
        
    x_axis = temp_x / np.linalg.norm(temp_x)
    y_axis = np.cross(z_axis, x_axis)
    
    print(f"X-axis: {x_axis}")
    print(f"Y-axis: {y_axis}")

    # Rotation matrix [x_axis, y_axis, z_axis]
    rot_matrix = np.column_stack((x_axis, y_axis, z_axis))
    print(f"Rotation Matrix:\n{rot_matrix}")
    
    # Convert to quaternion
    r = R.from_matrix(rot_matrix)
    quat = r.as_quat() # (x, y, z, w)
    print(f"Quaternion (x,y,z,w): {quat}")
    
    euler = r.as_euler('xyz', degrees=True)
    print(f"Euler (xyz degrees): {euler}")

    return quat

# Points from user log (Diagonal failure)
p1 = [-0.28260663481114756, 0.08363935448707392, 0.5611117538804555]
p2 = [-0.34704590398724094, 0.18848706415867697, 0.5139044903893399]

calculate_orientation_vector(p1, p2)
