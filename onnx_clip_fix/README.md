## Fix the Onnx Clip Node with Three Inputs Issue

It's used to fix the known issue Runtime Error: [Clamp layer has incorrect number of input ports](https://github.com/openvinotoolkit/openvino/issues/444)

In MobileNetV3 model convert from PaddlePaddle to Onnx, the Clip have three inputs:
```
input: Tensor
min: Constant
max: Constant
```

The onnx graph is then converted to Openvino IR. The .xml contains the following layer:

```
<layer id="3" name="5" type="Clamp" version="opset1">
	<data max="3.4028234663852886e+38" min="-3.4028234663852886e+38"/>
	<input>
		<port id="0">
			<dim>2</dim>
			<dim>4</dim>
		</port>
		<port id="1"/>
		<port id="2"/>
	</input>
	<output>
		<port id="3" precision="FP32">
		        <dim>2</dim>
			<dim>4</dim>
		</port>
	</output>
</layer>
```

The node will triger OpenVINO report error in running:

**RuntimeError: Clamp layer 5 with id: 3 has incorrect number of input ports**

This script will convert the Clip node from:
```
input: Tensor
min: Constant
max: Constant
```

to one input and two attributes:
```
input: Tensor
attribute:
  min: Tensor
  max: Tensor
```
## Prepare

Install onnx package

`pip install onnx`

## Install

Get the code

```
git clone https://github.com/arthw/oepnvino_tools.git
cd openvino_tools/onnx_clip_fix
```

## Usage
```
python onnx_clip_fix.py [input_model] [output_model]
```

Like
```
python onnx_clip_fix.py raw.onnx fixed.onnx
```
