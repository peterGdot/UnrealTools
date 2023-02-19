import bpy

bl_info = {
	"name": "Unreal Tools",
	"author": "Peter Grundmann (peterGdot)",
	"version": (0, 0, 1),
	"blender": (2, 80, 0),
	"location": "View3D > Sidebar > Edit Tab",
	"description": "Unreal Tools",
	"category": "Object",
}

def setBoundMaterial(obj, materialName):
	materialName = "Unreal Collision"
	
	if materialName in obj.data.materials:
		return
	
	urMat = None
	for mat in bpy.data.materials:
		 if mat.name == materialName:
			 urMat = mat
			 break
		 
	if not urMat:
		urMat = bpy.data.materials.new(materialName)
		urMat.diffuse_color = (1.0, 0.0, 0.5, 0.333)
		urMat.blend_method = "BLEND"
		
		urMat.use_nodes = True
		node_tree = urMat.node_tree
		nodes = node_tree.nodes
		bsdf = nodes.get("Principled BSDF")
		bsdf.inputs[0].default_value = (1.0, 0.0, 0.5, 0.333)
		bsdf.inputs[21].default_value = 0.2
		
	# add material to object
	obj.data.materials.clear()
	obj.data.materials.append(urMat)
	obj.active_material_index = 0 


def addBoundBox(context):
	selected = bpy.context.selected_objects

	for obj in selected:
		if obj.name.startswith('UBX_'): continue;
		if obj.name.startswith('USP_'): continue;
		# center origin
		bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
		# find destination (if any)
		name = "UBX_" + obj.name
		dest = bpy.context.scene.objects.get(name)
		if not dest:
			# add a bounding box cube
			bpy.ops.mesh.primitive_cube_add() 
			dest = bpy.context.active_object
			# name it unreal conform
			dest.name = name
			setBoundMaterial(dest, "Unreal Collision")
		
		# adjust center and boundries
		dest.location = obj.location
		dest.rotation_euler = obj.rotation_euler
		dest.dimensions = obj.dimensions


class UnrealBoundBoxOperator(bpy.types.Operator):
	"""Create a Unreal Bound Box collision mesh for each selected object."""
	bl_idname = "object.unreal_bound_box_operator"
	bl_label = "Unreal - Create Bounding Box"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return len(bpy.context.selected_objects) > 0

	def execute(self, context):
		addBoundBox(context)
		return {'FINISHED'}


def addBoundSphere(context):
	selected = bpy.context.selected_objects

	for obj in selected:
		if obj.name.startswith('UBX_'): continue;
		if obj.name.startswith('USP_'): continue;
		# center origin
		bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
		# find destination (if any)
		name = "USP_" + obj.name
		dest = bpy.context.scene.objects.get(name)
		if not dest:
			# add a bounding box cube
			bpy.ops.mesh.primitive_uv_sphere_add(segments = 16, ring_count=16, radius = obj.dimensions.length * 0.5, location = obj.location, rotation = obj.rotation_euler)
			dest = bpy.context.active_object
			bpy.ops.object.shade_smooth()
			# name it unreal conform
			dest.name = name
			setBoundMaterial(dest, "Unreal Collision")
		
		# adjust center and boundries
		# dest.location = obj.location
		# dest.rotation_euler = obj.rotation_euler
		# dest.dimensions = obj.dimensions


class UnrealBoundSphereOperator(bpy.types.Operator):
	"""Create a Unreal Bound Sphere collision mesh for each selected object."""
	bl_idname = "object.unreal_bound_sphere_operator"
	bl_label = "Unreal - Create Bounding Sphere"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return len(bpy.context.selected_objects) > 0

	def execute(self, context):
		addBoundSphere(context)
		return {'FINISHED'}


class OBJECT_MT_mymenu(bpy.types.Menu):
	bl_idname = 'object.unreal'
	bl_label = 'Unreal'

	def draw(self, context):
		layout = self.layout
		layout.operator(UnrealBoundBoxOperator.bl_idname)
		layout.operator(UnrealBoundSphereOperator.bl_idname)



def menu_func(self, context):
	self.layout.menu(OBJECT_MT_mymenu.bl_idname)

def register():
	bpy.utils.register_class(UnrealBoundBoxOperator)
	bpy.utils.register_class(UnrealBoundSphereOperator)
	bpy.utils.register_class(OBJECT_MT_mymenu)
	bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
	bpy.utils.unregister_class(UnrealBoundBoxOperator)
	bpy.utils.unregister_class(UnrealBoundSphereOperator)
	bpy.utils.unregister_class(OBJECT_MT_mymenu)
	bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
	register()
