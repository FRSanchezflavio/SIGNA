import React, { useState } from 'react';
import {
  Form,
  Input,
  Select,
  DatePicker,
  TimePicker,
  InputNumber,
  Button,
  Space,
  Collapse,
  message,
  Alert,
} from 'antd';
import {
  SaveOutlined,
  PlusOutlined,
  CloseOutlined,
  ClearOutlined,
} from '@ant-design/icons';
import dayjs from 'dayjs';

const { TextArea } = Input;
const { Option } = Select;
const { Panel } = Collapse;

interface FormularioRegistroProps {
  coordenadas: { lat: number; lng: number } | null;
  onSuccess: () => void;
  onCancel: () => void;
}

const FormularioRegistro: React.FC<FormularioRegistroProps> = ({
  coordenadas,
  onSuccess,
  onCancel,
}) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [caracteresResena, setCaracteresResena] = useState(0);

  const handleSubmit = async (values: any) => {
    setLoading(true);
    try {
      // TODO: Enviar datos a la API
      console.log('Datos del formulario:', values);
      console.log('Coordenadas:', coordenadas);

      message.success('Evento registrado exitosamente');
      form.resetFields();
      onSuccess();
    } catch (error) {
      message.error('Error al registrar el evento');
    } finally {
      setLoading(false);
    }
  };

  const handleResenaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setCaracteresResena(e.target.value.length);
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={handleSubmit}
      initialValues={{
        latitud: coordenadas?.lat,
        longitud: coordenadas?.lng,
      }}
    >
      <Alert
        message="Campos Obligatorios"
        description="Los campos marcados con (*) son obligatorios. Si no cuenta con información, el sistema registrará automáticamente 'NO CONSTA'."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />

      <Collapse defaultActiveKey={['seccion-a']} accordion>
        {/* SECCIÓN A: INFORMACIÓN ADMINISTRATIVA */}
        <Panel header="A. Información Administrativa" key="seccion-a">
          <Form.Item
            label="Nº de Imagen/Sumario o Fecha de Memorándum"
            name="numero_sumario"
            rules={[{ required: true, message: 'Campo obligatorio' }]}
          >
            <Input placeholder="Ej: 001/2025" />
          </Form.Item>

          <Form.Item
            label="Jurisdicción donde tuvo lugar el delito"
            name="jurisdiccion_id"
            rules={[{ required: true, message: 'Campo obligatorio' }]}
          >
            <Select placeholder="Seleccione jurisdicción">
              <Option value={1}>Centro</Option>
              <Option value={2}>Norte</Option>
              <Option value={3}>Sur</Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="Dependencia Interviniente"
            name="dependencia_id"
            rules={[{ required: true, message: 'Campo obligatorio' }]}
          >
            <Select placeholder="Seleccione dependencia">
              <Option value={1}>Comisaría 1ra</Option>
              <Option value={2}>Comisaría 2da</Option>
            </Select>
          </Form.Item>
        </Panel>

        {/* SECCIÓN B: DATOS TEMPORALES */}
        <Panel header="B. Datos Temporales" key="seccion-b">
          <Form.Item
            label="Fecha del Delito"
            name="fecha_delito"
            rules={[{ required: true, message: 'Campo obligatorio' }]}
          >
            <DatePicker style={{ width: '100%' }} format="DD/MM/YYYY" />
          </Form.Item>

          <Form.Item
            label="Hora del Delito"
            name="hora_delito"
            rules={[{ required: true, message: 'Campo obligatorio' }]}
          >
            <TimePicker style={{ width: '100%' }} format="HH:mm" />
          </Form.Item>

          <Form.Item label="Franja Horaria" name="franja_horaria">
            <Select placeholder="Seleccione franja horaria">
              <Option value="MADRUGADA">Madrugada (00:00 - 05:59)</Option>
              <Option value="MAÑANA">Mañana (06:00 - 11:59)</Option>
              <Option value="TARDE">Tarde (12:00 - 17:59)</Option>
              <Option value="NOCHE">Noche (18:00 - 23:59)</Option>
            </Select>
          </Form.Item>
        </Panel>

        {/* SECCIÓN C: INFORMACIÓN DEL LUGAR */}
        <Panel header="C. Información del Lugar" key="seccion-c">
          <Form.Item
            label="Dirección donde ocurrió el delito"
            name="direccion"
            rules={[{ required: true, message: 'Campo obligatorio' }]}
          >
            <Input placeholder="Calle, número, barrio" />
          </Form.Item>

          <Form.Item label="Latitud" name="latitud">
            <Input disabled />
          </Form.Item>

          <Form.Item label="Longitud" name="longitud">
            <Input disabled />
          </Form.Item>

          <Form.Item label="Lugar donde tuvo lugar el delito" name="lugar_tipo">
            <Select placeholder="Seleccione tipo de lugar">
              <Option value="VÍA PÚBLICA">Vía Pública</Option>
              <Option value="DOMICILIO PARTICULAR">Domicilio Particular</Option>
              <Option value="COMERCIO">Comercio</Option>
              <Option value="ENTIDAD BANCARIA">Entidad Bancaria</Option>
              <Option value="INSTITUCIÓN PÚBLICA">Institución Pública</Option>
              <Option value="VEHÍCULO">Vehículo</Option>
              <Option value="OTRO">Otro</Option>
            </Select>
          </Form.Item>
        </Panel>

        {/* SECCIÓN D: CARACTERÍSTICAS DEL DELITO */}
        <Panel header="D. Características del Delito" key="seccion-d">
          <Form.Item
            label="Delito Cometido"
            name="tipo_delito_id"
            rules={[{ required: true, message: 'Campo obligatorio' }]}
          >
            <Select placeholder="Seleccione tipo de delito">
              <Option value={1}>Robo</Option>
              <Option value={2}>Robo Agravado</Option>
              <Option value={3}>Hurto</Option>
              <Option value={4}>Homicidio</Option>
              <Option value={5}>Estafa</Option>
              <Option value={6}>189 BIS</Option>
              <Option value={7}>Abigeato</Option>
              <Option value={8}>Otro</Option>
            </Select>
          </Form.Item>

          <Form.Item label="Modus Operandi" name="modus_operandi">
            <Select placeholder="Seleccione modus operandi">
              <Option value="ARIETE">Ariete</Option>
              <Option value="ARREBATO">Arrebato</Option>
              <Option value="ASALTANTE">Asaltante</Option>
              <Option value="ENTRADERA">Entradera</Option>
              <Option value="OTRO">Otro</Option>
            </Select>
          </Form.Item>

          <Form.Item label="Vehículos Utilizados" name="vehiculo_utilizado">
            <Select placeholder="Seleccione vehículo">
              <Option value="MOTOCICLETA">Motocicleta</Option>
              <Option value="AUTOMÓVIL">Automóvil</Option>
              <Option value="CAMIONETA">Camioneta</Option>
              <Option value="BICICLETA">Bicicleta</Option>
              <Option value="A PIE">A Pie</Option>
              <Option value="OTRO">Otro</Option>
            </Select>
          </Form.Item>
        </Panel>

        {/* SECCIÓN F: RESEÑA DEL HECHO */}
        <Panel header="F. Reseña del Hecho" key="seccion-f">
          <Form.Item
            label="Breve reseña del hecho"
            name="resena_hecho"
            rules={[
              { required: true, message: 'Campo obligatorio' },
              { max: 254, message: 'Máximo 254 caracteres' },
            ]}
          >
            <TextArea
              rows={4}
              maxLength={254}
              onChange={handleResenaChange}
              placeholder="Describa los detalles más relevantes del hecho..."
            />
          </Form.Item>
          <div
            className={`character-counter ${
              caracteresResena > 240 ? 'warning' : ''
            }`}
          >
            {caracteresResena} / 254 caracteres
          </div>
        </Panel>
      </Collapse>

      <div style={{ marginTop: 24 }}>
        <Space>
          <Button
            type="primary"
            icon={<SaveOutlined />}
            htmlType="submit"
            loading={loading}
          >
            Guardar
          </Button>
          <Button icon={<SaveOutlined />} onClick={() => form.submit()}>
            Guardar y Nuevo
          </Button>
          <Button icon={<ClearOutlined />} onClick={() => form.resetFields()}>
            Limpiar
          </Button>
          <Button icon={<CloseOutlined />} onClick={onCancel}>
            Cancelar
          </Button>
        </Space>
      </div>
    </Form>
  );
};

export default FormularioRegistro;
