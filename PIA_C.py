import pandas as pd
import os
from tabulate import tabulate
import sys

def limpiar_valor(valor):
    if isinstance(valor, str):
        valor = valor.replace('$', '').replace(',', '')
    
    num_val = pd.to_numeric(valor, errors='coerce')
    
    if pd.isna(num_val):
        return 0.0
    return num_val

def pedir_numero(prompt, es_flotante=True):
    while True:
        valor_str = input(f"  > {prompt}: ")
        try:
            if es_flotante:
                valor_num = float(valor_str)
            else:
                valor_num = int(valor_str)
            return valor_num
        except ValueError:
            print(f"Error: '{valor_str}' no es un número válido. Intenta de nuevo.")

def pedir_datos_usuario():
    datos = {}
    
    try:
        datos['balance_2015'] = {
            'efectivo': 200000.0,
            'clientes': 90000.0,
            'deudores_diversos': 15000.0,
            'funcionarios_empleados': 5000.0,
            'inv_materiales_costo': 65000.0,
            'inv_prod_terminado_costo': 180000.0,
            'terreno': 1500000.0,
            'planta_equipo_bruto': 2200000.0,
            'dep_acumulada': 700000.0,
            
            'proveedores': 75000.0,
            'documentos_por_pagar': 800000.0,
            'isr_por_pagar': 40000.0,
            'prestamos_bancarios_lp': 1000000.0,
            'capital_contribuido': 1000000.0,
            'capital_ganado': 640000.0,
        }

        print("\n--- 2. Requerimiento de Materiales y MOD (por unidad de producto) ---")
        uso_materiales = {}
        mod = {}
        for prod in ['XS', 'X', 'XL']:
            print(f"\nProducto {prod}:")
            uso_materiales[f'{prod}_mat_A'] = pedir_numero(f"Uso de Material A (metros) para {prod}")
            uso_materiales[f'{prod}_mat_B'] = pedir_numero(f"Uso de Material B (metros) para {prod}")
            uso_materiales[f'{prod}_mat_C'] = pedir_numero(f"Uso de Material C (piezas) para {prod}")
            mod[f'{prod}_horas'] = pedir_numero(f"Horas de MOD para {prod}")
        
        datos['uso_materiales'] = uso_materiales
        
        print("\nCosto de Mano de Obra (MOD):")
        mod['tarifa_hr_1S'] = pedir_numero("Tarifa por Hora MOD (1er Semestre)")
        mod['tarifa_hr_2S'] = pedir_numero("Tarifa por Hora MOD (2do Semestre)")
        datos['mod'] = mod

        print("\n--- 3. Inventarios (Unidades y Costos) ---")
        inventarios = {}
        print("\nMaterial A:")
        inventarios['mat_A_inicial_u'] = pedir_numero("Inventario Inicial (Uds)", es_flotante=False)
        inventarios['mat_A_final_u'] = pedir_numero("Inventario Final (Uds)", es_flotante=False)
        inventarios['costo_mat_A_1S'] = pedir_numero("Costo Unitario (1er Semestre)")
        inventarios['costo_mat_A_2S'] = pedir_numero("Costo Unitario (2do Semestre)")
        
        print("\nMaterial B:")
        inventarios['mat_B_inicial_u'] = pedir_numero("Inventario Inicial (Uds)", es_flotante=False)
        inventarios['mat_B_final_u'] = pedir_numero("Inventario Final (Uds)", es_flotante=False)
        inventarios['costo_mat_B_1S'] = pedir_numero("Costo Unitario (1er Semestre)")
        inventarios['costo_mat_B_2S'] = pedir_numero("Costo Unitario (2do Semestre)")

        print("\nMaterial C:")
        inventarios['mat_C_inicial_u'] = pedir_numero("Inventario Inicial (Uds)", es_flotante=False)
        inventarios['mat_C_final_u'] = pedir_numero("Inventario Final (Uds)", es_flotante=False)
        inventarios['costo_mat_C_1S'] = pedir_numero("Costo Unitario (1er Semestre)")
        inventarios['costo_mat_C_2S'] = pedir_numero("Costo Unitario (2do Semestre)")

        print("\nProducto Terminado XS:")
        inventarios['pt_XS_inicial_u'] = pedir_numero("Inventario Inicial (Uds)", es_flotante=False)
        inventarios['pt_XS_final_u'] = pedir_numero("Inventario Final (Uds)", es_flotante=False)
        
        print("\nProducto Terminado X:")
        inventarios['pt_X_inicial_u'] = pedir_numero("Inventario Inicial (Uds)", es_flotante=False)
        inventarios['pt_X_final_u'] = pedir_numero("Inventario Final (Uds)", es_flotante=False)

        print("\nProducto Terminado XL:")
        inventarios['pt_XL_inicial_u'] = pedir_numero("Inventario Inicial (Uds)", es_flotante=False)
        inventarios['pt_XL_final_u'] = pedir_numero("Inventario Final (Uds)", es_flotante=False)
        
        inventarios['mat_A_final_1S_u'] = inventarios['mat_A_inicial_u']
        inventarios['mat_B_final_1S_u'] = inventarios['mat_B_inicial_u']
        inventarios['mat_C_final_1S_u'] = inventarios['mat_C_inicial_u']
        inventarios['pt_XS_final_1S_u'] = inventarios['pt_XS_inicial_u']
        inventarios['pt_X_final_1S_u'] = inventarios['pt_X_inicial_u']
        inventarios['pt_XL_final_1S_u'] = inventarios['pt_XL_inicial_u']
        datos['inventarios'] = inventarios

        print("\n--- 4. Ventas (Precios y Unidades) ---")
        ventas = {}
        print("\nProducto XS:")
        ventas['XS_precio_1S'] = pedir_numero("Precio de Venta (1er Semestre)")
        ventas['XS_unidades_1S'] = pedir_numero("Ventas Planeadas (Uds) (1er Semestre)", es_flotante=False)
        ventas['XS_precio_2S'] = pedir_numero("Precio de Venta (2do Semestre)")
        ventas['XS_unidades_2S'] = pedir_numero("Ventas Planeadas (Uds) (2do Semestre)", es_flotante=False)
        
        print("\nProducto X:")
        ventas['X_precio_1S'] = pedir_numero("Precio de Venta (1er Semestre)")
        ventas['X_unidades_1S'] = pedir_numero("Ventas Planeadas (Uds) (1er Semestre)", es_flotante=False)
        ventas['X_precio_2S'] = pedir_numero("Precio de Venta (2do Semestre)")
        ventas['X_unidades_2S'] = pedir_numero("Ventas Planeadas (Uds) (2do Semestre)", es_flotante=False)

        print("\nProducto XL:")
        ventas['XL_precio_1S'] = pedir_numero("Precio de Venta (1er Semestre)")
        ventas['XL_unidades_1S'] = pedir_numero("Ventas Planeadas (Uds) (1er Semestre)", es_flotante=False)
        ventas['XL_precio_2S'] = pedir_numero("Precio de Venta (2do Semestre)")
        ventas['XL_unidades_2S'] = pedir_numero("Ventas Planeadas (Uds) (2do Semestre)", es_flotante=False)
        datos['ventas'] = ventas

        print("\n--- 5. Gastos de Administración y Ventas (GAV) ---")
        gav = {}
        gav['depreciacion'] = pedir_numero("Depreciación (Anual)")
        gav['sueldos'] = pedir_numero("Sueldos y Salarios (Anual)")
        gav['comisiones_tasa'] = pedir_numero("Tasa de Comisiones (ej: 0.01 para 1%)")
        gav['varios_1S'] = pedir_numero("Gastos Varios (1er Semestre)")
        gav['varios_2S'] = pedir_numero("Gastos Varios (2do Semestre)")
        gav['intereses'] = pedir_numero("Intereses por Préstamo (Anual)")
        datos['gav'] = gav
        
        print("\n--- 6. Gastos Indirectos de Fabricación (GIF) ---")
        gif = {}
        gif['depreciacion'] = pedir_numero("Depreciación (Anual)")
        gif['seguros'] = pedir_numero("Seguros (Anual)")
        gif['manto_1S'] = pedir_numero("Mantenimiento (1er Semestre)")
        gif['manto_2S'] = pedir_numero("Mantenimiento (2do Semestre)")
        gif['energeticos_1S'] = pedir_numero("Energéticos (1er Semestre)")
        gif['energeticos_2S'] = pedir_numero("Energéticos (2do Semestre)")
        gif['varios'] = pedir_numero("Gastos Varios (Anual)")
        datos['gif'] = gif
        
        print("\n--- 7. Políticas de la Empresa (Constantes) ---")
        print("Cargando políticas constantes...")
        datos['politicas'] = {
            'tasa_isr': 0.30,
            'tasa_ptu': 0.10,
            'tasa_isr_ptu': 0.30 + 0.10,
            'pago_proveedores_contado': 0.60,
            'cobranza_contado': 0.75,
            'compra_activo_fijo': 110000.00
        }
        print("  > Tasa ISR: 30%")
        print("  > Tasa PTU: 10%")
        print("  > Pago a Proveedores (Contado): 60%")
        print("  > Cobranza (Contado): 75%")
        print("  > Compra Activo Fijo: $110,000.00")

    except KeyboardInterrupt:
        print("\n\nEntrada de datos cancelada. Saliendo del programa.")
        sys.exit()
    except Exception as e:
        print(f"\nError inesperado durante la entrada de datos: {e}")
        sys.exit()

    return datos

def f_int(n): return f"{n:,.0f}"
def f_mon(n): return f"{n:,.2f}"

def calcular_cedula_1_ventas(d, cedulas):
    v = d['ventas']
    ventas_data = {
        'XS': {
            'U_1S': v['XS_unidades_1S'], 'P_1S': v['XS_precio_1S'], 'V_1S': v['XS_unidades_1S'] * v['XS_precio_1S'],
            'U_2S': v['XS_unidades_2S'], 'P_2S': v['XS_precio_2S'], 'V_2S': v['XS_unidades_2S'] * v['XS_precio_2S'],
        },
        'X': {
            'U_1S': v['X_unidades_1S'], 'P_1S': v['X_precio_1S'], 'V_1S': v['X_unidades_1S'] * v['X_precio_1S'],
            'U_2S': v['X_unidades_2S'], 'P_2S': v['X_precio_2S'], 'V_2S': v['X_unidades_2S'] * v['X_precio_2S'],
        },
        'XL': {
            'U_1S': v['XL_unidades_1S'], 'P_1S': v['XL_precio_1S'], 'V_1S': v['XL_unidades_1S'] * v['XL_precio_1S'],
            'U_2S': v['XL_unidades_2S'], 'P_2S': v['XL_precio_2S'], 'V_2S': v['XL_unidades_2S'] * v['XL_precio_2S'],
        }
    }
    for prod in ventas_data:
        ventas_data[prod]['U_Total'] = ventas_data[prod]['U_1S'] + ventas_data[prod]['U_2S']
        ventas_data[prod]['V_Total'] = ventas_data[prod]['V_1S'] + ventas_data[prod]['V_2S']
    
    tabla_ventas = []
    headers = ["Concepto", "1er. Semestre", "2do. Semestre", "Total 2016"]

    v_xs = ventas_data['XS']
    tabla_ventas.append(["PRODUCTO XS", "", "", ""])
    tabla_ventas.append([f"  {'Unidades a Vender':<20}", f_int(v_xs['U_1S']), f_int(v_xs['U_2S']), f_int(v_xs['U_Total'])])
    tabla_ventas.append([f"  {'Precio de Venta':<20}", f_mon(v_xs['P_1S']), f_mon(v_xs['P_2S']), "-"])
    tabla_ventas.append([f"  {'Importe de Venta':<20}", f_mon(v_xs['V_1S']), f_mon(v_xs['V_2S']), f_mon(v_xs['V_Total'])])
    tabla_ventas.append([])

    v_x = ventas_data['X']
    tabla_ventas.append(["PRODUCTO X", "", "", ""])
    tabla_ventas.append([f"  {'Unidades a Vender':<20}", f_int(v_x['U_1S']), f_int(v_x['U_2S']), f_int(v_x['U_Total'])])
    tabla_ventas.append([f"  {'Precio de Venta':<20}", f_mon(v_x['P_1S']), f_mon(v_x['P_2S']), "-"])
    tabla_ventas.append([f"  {'Importe de Venta':<20}", f_mon(v_x['V_1S']), f_mon(v_x['V_2S']), f_mon(v_x['V_Total'])])
    tabla_ventas.append([])
    
    v_xl = ventas_data['XL']
    tabla_ventas.append(["PRODUCTO XL", "", "", ""])
    tabla_ventas.append([f"  {'Unidades a Vender':<20}", f_int(v_xl['U_1S']), f_int(v_xl['U_2S']), f_int(v_xl['U_Total'])])
    tabla_ventas.append([f"  {'Precio de Venta':<20}", f_mon(v_xl['P_1S']), f_mon(v_xl['P_2S']), "-"])
    tabla_ventas.append([f"  {'Importe de Venta':<20}", f_mon(v_xl['V_1S']), f_mon(v_xl['V_2S']), f_mon(v_xl['V_Total'])])
    tabla_ventas.append([])

    total_ventas_1s = v_xs['V_1S'] + v_x['V_1S'] + v_xl['V_1S']
    total_ventas_2s = v_xs['V_2S'] + v_x['V_2S'] + v_xl['V_2S']
    total_ventas_2016 = sum(ventas_data[p]['V_Total'] for p in ventas_data)

    tabla_ventas.append(["Total de Ventas por Semestre", f_mon(total_ventas_1s), f_mon(total_ventas_2s), f_mon(total_ventas_2016)])
    
    cedulas['1_ventas'] = {
        'tabla': tabla_ventas,
        'headers': headers,
        'total_ventas_2016': total_ventas_2016,
        'ventas_data': ventas_data,
        'ventas_1S_U': {'XS': v_xs['U_1S'], 'X': v_x['U_1S'], 'XL': v_xl['U_1S']},
        'ventas_2S_U': {'XS': v_xs['U_2S'], 'X': v_x['U_2S'], 'XL': v_xl['U_2S']}
    }
    return cedulas

def calcular_cedula_2_cobranza(d, cedulas):
    pol = d['politicas']
    b15 = d['balance_2015']
    total_ventas_2016 = cedulas['1_ventas']['total_ventas_2016']
    
    cobranza_2016 = total_ventas_2016 * pol['cobranza_contado']
    saldo_clientes_final = total_ventas_2016 * (1 - pol['cobranza_contado'])
    
    cobranza_2015 = b15['clientes']
    total_entradas = cobranza_2016 + cobranza_2015
    
    headers_cobranza = ["Descripción", "Importe", "Total"]
    
    tabla_saldo_clientes = [
        ["Saldo de clientes 31-Dic-2015", f_mon(b15['clientes']), ""],
        ["Ventas 2016", f_mon(total_ventas_2016), ""],
        ["Total de Clientes", "", f_mon(b15['clientes'] + total_ventas_2016)],
        ["Cobranza 2016 (75%)", f"({f_mon(cobranza_2016)})", ""],
        ["Cobranza 2015 (100%)", f"({f_mon(cobranza_2015)})", ""],
        ["Saldo de Clientes 31-Dic-2016", "", f_mon(saldo_clientes_final)],
    ]
    
    tabla_flujo_entradas = [
        ["Cobranza 2016", f_mon(cobranza_2016), ""],
        ["Cobranza 2015 (Saldo Inicial)", f_mon(cobranza_2015), ""],
        ["Total de Entradas", "", f_mon(total_entradas)],
    ]
    
    cedulas['2_cobranza'] = {
        'tabla_saldo_clientes': tabla_saldo_clientes,
        'tabla_flujo_entradas': tabla_flujo_entradas,
        'headers': headers_cobranza,
        'total_entradas': total_entradas,
        'saldo_clientes_final': saldo_clientes_final
    }
    return cedulas

def calcular_cedula_3_produccion(d, cedulas):
    i = d['inventarios']
    v = cedulas['1_ventas']
    
    prod_1S_XS = v['ventas_1S_U']['XS']
    prod_1S_X = v['ventas_1S_U']['X']
    prod_1S_XL = v['ventas_1S_U']['XL']
    
    prod_2S_XS = v['ventas_2S_U']['XS'] + i['pt_XS_final_u'] - i['pt_XS_inicial_u']
    prod_2S_X = v['ventas_2S_U']['X'] + i['pt_X_final_u'] - i['pt_X_inicial_u']
    prod_2S_XL = v['ventas_2S_U']['XL'] + i['pt_XL_final_u'] - i['pt_XL_inicial_u']

    prod_total_XS = prod_1S_XS + prod_2S_XS
    prod_total_X = prod_1S_X + prod_2S_X
    prod_total_XL = prod_1S_XL + prod_2S_XL

    prod_data = {
        'XS': {
            'Ventas_U': v['ventas_data']['XS']['U_Total'],
            'Inv_Final_U': i['pt_XS_final_u'],
            'Inv_Inicial_U': i['pt_XS_inicial_u'],
            'Unidades_a_Producir': prod_total_XS
        },
        'X': {
            'Ventas_U': v['ventas_data']['X']['U_Total'],
            'Inv_Final_U': i['pt_X_final_u'],
            'Inv_Inicial_U': i['pt_X_inicial_u'],
            'Unidades_a_Producir': prod_total_X
        },
        'XL': {
            'Ventas_U': v['ventas_data']['XL']['U_Total'],
            'Inv_Final_U': i['pt_XL_final_u'],
            'Inv_Inicial_U': i['pt_XL_inicial_u'],
            'Unidades_a_Producir': prod_total_XL
        }
    }
    for prod in prod_data:
        prod_data[prod]['Total_Necesidad'] = prod_data[prod]['Ventas_U'] + prod_data[prod]['Inv_Final_U']

    
    df_produccion = pd.DataFrame(prod_data).T
    
    column_order = ['Ventas_U', 'Inv_Final_U', 'Total_Necesidad', 'Inv_Inicial_U', 'Unidades_a_Producir']
    column_headers = [
        "(+) Ventas (Uds)", 
        "(+) Inv. Final Deseado (Uds)", 
        "(=) Total Necesidad", 
        "(-) Inv. Inicial (Uds)", 
        "(=) Uds a Producir"
    ]
    
    df_produccion = df_produccion[column_order]
    df_produccion.columns = column_headers
    
    df_produccion.loc['Total'] = df_produccion.sum()
    
    cedulas['3_produccion'] = {
        'dataframe': df_produccion,
        'produccion_1S': {'XS': prod_1S_XS, 'X': prod_1S_X, 'XL': prod_1S_XL},
        'produccion_2S': {'XS': prod_2S_XS, 'X': prod_2S_X, 'XL': prod_2S_XL},
        'produccion_total': {'XS': prod_total_XS, 'X': prod_total_X, 'XL': prod_total_XL}
    }
    return cedulas

def calcular_cedula_4_req_materiales(d, cedulas):
    u = d['uso_materiales']
    p = cedulas['3_produccion']
    
    req_A_1S_XS = p['produccion_1S']['XS'] * u['XS_mat_A']
    req_A_1S_X  = p['produccion_1S']['X']  * u['X_mat_A']
    req_A_1S_XL = p['produccion_1S']['XL'] * u['XL_mat_A']
    total_req_A_1S = req_A_1S_XS + req_A_1S_X + req_A_1S_XL
    
    req_B_1S_XS = p['produccion_1S']['XS'] * u['XS_mat_B']
    req_B_1S_X  = p['produccion_1S']['X']  * u['X_mat_B']
    req_B_1S_XL = p['produccion_1S']['XL'] * u['XL_mat_B']
    total_req_B_1S = req_B_1S_XS + req_B_1S_X + req_B_1S_XL
    
    req_C_1S_XS = p['produccion_1S']['XS'] * u['XS_mat_C']
    req_C_1S_X  = p['produccion_1S']['X']  * u['X_mat_C']
    req_C_1S_XL = p['produccion_1S']['XL'] * u['XL_mat_C']
    total_req_C_1S = req_C_1S_XS + req_C_1S_X + req_C_1S_XL

    req_A_2S_XS = p['produccion_2S']['XS'] * u['XS_mat_A']
    req_A_2S_X  = p['produccion_2S']['X']  * u['X_mat_A']
    req_A_2S_XL = p['produccion_2S']['XL'] * u['XL_mat_A']
    total_req_A_2S = req_A_2S_XS + req_A_2S_X + req_A_2S_XL
    
    req_B_2S_XS = p['produccion_2S']['XS'] * u['XS_mat_B']
    req_B_2S_X  = p['produccion_2S']['X']  * u['X_mat_B']
    req_B_2S_XL = p['produccion_2S']['XL'] * u['XL_mat_B']
    total_req_B_2S = req_B_2S_XS + req_B_2S_X + req_B_2S_XL
    
    req_C_2S_XS = p['produccion_2S']['XS'] * u['XS_mat_C']
    req_C_2S_X  = p['produccion_2S']['X']  * u['X_mat_C']
    req_C_2S_XL = p['produccion_2S']['XL'] * u['XL_mat_C']
    total_req_C_2S = req_C_2S_XS + req_C_2S_X + req_C_2S_XL

    req_mat_A = total_req_A_1S + total_req_A_2S
    req_mat_B = total_req_B_1S + total_req_B_2S
    req_mat_C = total_req_C_1S + total_req_C_2S
    
    headers_req = [
        "Producto", 
        "Uds. a Producir", 
        "Req. Mat. A", "Total A", 
        "Req. Mat. B", "Total B",
        "Req. Mat. C", "Total C"
    ]
    
    tabla_req = [
        [
            "XS", f_int(p['produccion_total']['XS']), f_mon(u['XS_mat_A']), f_mon(p['produccion_total']['XS'] * u['XS_mat_A']),
            f_mon(u['XS_mat_B']), f_mon(p['produccion_total']['XS'] * u['XS_mat_B']),
            f_mon(u['XS_mat_C']), f_mon(p['produccion_total']['XS'] * u['XS_mat_C'])
        ],
        [
            "X", f_int(p['produccion_total']['X']), f_mon(u['X_mat_A']), f_mon(p['produccion_total']['X'] * u['X_mat_A']),
            f_mon(u['X_mat_B']), f_mon(p['produccion_total']['X'] * u['X_mat_B']),
            f_mon(u['X_mat_C']), f_mon(p['produccion_total']['X'] * u['X_mat_C'])
        ],
        [
            "XL", f_int(p['produccion_total']['XL']), f_mon(u['XL_mat_A']), f_mon(p['produccion_total']['XL'] * u['XL_mat_A']),
            f_mon(u['XL_mat_B']), f_mon(p['produccion_total']['XL'] * u['XL_mat_B']),
            f_mon(u['XL_mat_C']), f_mon(p['produccion_total']['XL'] * u['XL_mat_C'])
        ],
        [
            "Total Requerido:", "", "", f_mon(req_mat_A), "", f_mon(req_mat_B), "", f_mon(req_mat_C)
        ]
    ]

    cedulas['4_req_materiales'] = {
        'tabla': tabla_req,
        'headers': headers_req,
        'req_mat_A_1S': total_req_A_1S, 'req_mat_B_1S': total_req_B_1S, 'req_mat_C_1S': total_req_C_1S,
        'req_mat_A_2S': total_req_A_2S, 'req_mat_B_2S': total_req_B_2S, 'req_mat_C_2S': total_req_C_2S,
    }
    return cedulas

def calcular_cedula_5_compras(d, cedulas):
    i = d['inventarios']
    r = cedulas['4_req_materiales']
    
    comprar_mat_A_u_1S = r['req_mat_A_1S']
    comprar_mat_B_u_1S = r['req_mat_B_1S']
    comprar_mat_C_u_1S = r['req_mat_C_1S']
    
    comprar_mat_A_u_2S = r['req_mat_A_2S'] + i['mat_A_final_u'] - i['mat_A_inicial_u']
    comprar_mat_B_u_2S = r['req_mat_B_2S'] + i['mat_B_final_u'] - i['mat_B_inicial_u']
    comprar_mat_C_u_2S = r['req_mat_C_2S'] + i['mat_C_final_u'] - i['mat_C_inicial_u']

    importe_compra_A_1S = comprar_mat_A_u_1S * i['costo_mat_A_1S']
    importe_compra_B_1S = comprar_mat_B_u_1S * i['costo_mat_B_1S']
    importe_compra_C_1S = comprar_mat_C_u_1S * i['costo_mat_C_1S']

    importe_compra_A_2S = comprar_mat_A_u_2S * i['costo_mat_A_2S']
    importe_compra_B_2S = comprar_mat_B_u_2S * i['costo_mat_B_2S']
    importe_compra_C_2S = comprar_mat_C_u_2S * i['costo_mat_C_2S']

    total_compras_u_A = comprar_mat_A_u_1S + comprar_mat_A_u_2S
    total_compras_u_B = comprar_mat_B_u_1S + comprar_mat_B_u_2S
    total_compras_u_C = comprar_mat_C_u_1S + comprar_mat_C_u_2S
    
    total_importe_A = importe_compra_A_1S + importe_compra_A_2S
    total_importe_B = importe_compra_B_1S + importe_compra_B_2S
    total_importe_C = importe_compra_C_1S + importe_compra_C_2S
    total_compras = total_importe_A + total_importe_B + total_importe_C
    
    headers_compras = [ "Concepto", "Material A", "Material B", "Material C", "Total" ]
    
    tabla_compras = [
        ["Requerimiento 1S (Uds)", f_int(r['req_mat_A_1S']), f_int(r['req_mat_B_1S']), f_int(r['req_mat_C_1S']), ""],
        ["Requerimiento 2S (Uds)", f_int(r['req_mat_A_2S']), f_int(r['req_mat_B_2S']), f_int(r['req_mat_C_2S']), ""],
        [
            "(+) Inv. Final (Uds)",
            f_int(i['mat_A_final_u']),
            f_int(i['mat_B_final_u']),
            f_int(i['mat_C_final_u']),
            ""
        ],
        [
            "(-) Inv. Inicial (Uds)",
            f"({f_int(i['mat_A_inicial_u'])})",
            f"({f_int(i['mat_B_inicial_u'])})",
            f"({f_int(i['mat_C_inicial_u'])})",
            ""
        ],
        [
            "(=) Total Uds a Comprar",
            f_int(total_compras_u_A),
            f_int(total_compras_u_B),
            f_int(total_compras_u_C),
            ""
        ],
        ["---", "---", "---", "---", "---"],
        ["Importe Compra 1S", f_mon(importe_compra_A_1S), f_mon(importe_compra_B_1S), f_mon(importe_compra_C_1S), ""],
        ["Importe Compra 2S", f_mon(importe_compra_A_2S), f_mon(importe_compra_B_2S), f_mon(importe_compra_C_2S), ""],
        [
            "(=) Importe Total Compra",
            f_mon(total_importe_A),
            f_mon(total_importe_B),
            f_mon(total_importe_C),
            f_mon(total_compras)
        ],
    ]
    
    cedulas['5_compras'] = {
        'tabla': tabla_compras,
        'headers': headers_compras,
        'total_compras': total_compras,
        'costo_inv_final_A': i['costo_mat_A_2S'],
        'costo_inv_final_B': i['costo_mat_B_2S'],
        'costo_inv_final_C': i['costo_mat_C_2S'],
    }
    return cedulas

def calcular_cedula_6_proveedores(d, cedulas):
    b15 = d['balance_2015']
    pol = d['politicas']
    total_compras = cedulas['5_compras']['total_compras']
    
    pago_proveedores_2016 = total_compras * pol['pago_proveedores_contado']
    saldo_proveedores_final = total_compras * (1 - pol['pago_proveedores_contado'])

    pago_proveedores_2015 = b15['proveedores']
    pago_proveedores_total = pago_proveedores_2016 + pago_proveedores_2015
    
    headers_prov = ["Descripción", "Importe", "Total"]
    
    tabla_saldo_prov = [
        ["Saldo de Proveedores 31-Dic-2015", f_mon(b15['proveedores']), ""],
        ["(+) Compras 2016", f_mon(total_compras), ""],
        ["(=) Total Proveedores", "", f_mon(b15['proveedores'] + total_compras)],
        ["(-) Pago Contado 2016 (60%)", f"({f_mon(pago_proveedores_2016)})", ""],
        ["(-) Pago Saldo 2015 (100%)", f"({f_mon(pago_proveedores_2015)})", ""],
        ["(=) Saldo Final Proveedores", "", f_mon(saldo_proveedores_final)],
    ]
    
    tabla_flujo_salidas = [
        ["Pago Contado 2016", f_mon(pago_proveedores_2016), ""],
        ["(+) Pago Saldo 2015", f_mon(pago_proveedores_2015), ""],
        ["(=) Total de Pago a Proveedores", "", f_mon(pago_proveedores_total)],
    ]
    
    cedulas['6_proveedores'] = {
        'tabla_saldo_prov': tabla_saldo_prov,
        'tabla_flujo_salidas': tabla_flujo_salidas,
        'headers': headers_prov,
        'pago_proveedores_total': pago_proveedores_total,
        'saldo_proveedores_final': saldo_proveedores_final
    }
    return cedulas

def calcular_cedula_7_mod(d, cedulas):
    m = d['mod']
    p = cedulas['3_produccion']
    
    horas_1S_XS = p['produccion_1S']['XS'] * m['XS_horas']
    horas_1S_X  = p['produccion_1S']['X']  * m['X_horas']
    horas_1S_XL = p['produccion_1S']['XL'] * m['XL_horas']
    total_horas_1S = horas_1S_XS + horas_1S_X + horas_1S_XL
    importe_1S = total_horas_1S * m['tarifa_hr_1S']

    horas_2S_XS = p['produccion_2S']['XS'] * m['XS_horas']
    horas_2S_X  = p['produccion_2S']['X']  * m['X_horas']
    horas_2S_XL = p['produccion_2S']['XL'] * m['XL_horas']
    total_horas_2S = horas_2S_XS + horas_2S_X + horas_2S_XL
    importe_2S = total_horas_2S * m['tarifa_hr_2S']
    
    total_horas_mod = total_horas_1S + total_horas_2S
    importe_total_mod = importe_1S + importe_2S
    
    headers_mod = [
        "Producto",
        "Uds. a Producir",
        "Horas x Unidad",
        "Total Horas",
        "Importe MOD"
    ]
    
    tabla_mod = [
        [
            "XS", f_int(p['produccion_total']['XS']), f_mon(m['XS_horas']),
            f_int(horas_1S_XS + horas_2S_XS), "-"
        ],
        [
            "X", f_int(p['produccion_total']['X']), f_mon(m['X_horas']),
            f_int(horas_1S_X + horas_2S_X), "-"
        ],
        [
            "XL", f_int(p['produccion_total']['XL']), f_mon(m['XL_horas']),
            f_int(horas_1S_XL + horas_2S_XL), "-"
        ],
        ["---", "---", "---", "---", "---"],
        ["Costo 1S", "", f"Total Horas 1S: {f_int(total_horas_1S)}", f"Tarifa: {f_mon(m['tarifa_hr_1S'])}", f_mon(importe_1S)],
        ["Costo 2S", "", f"Total Horas 2S: {f_int(total_horas_2S)}", f"Tarifa: {f_mon(m['tarifa_hr_2S'])}", f_mon(importe_2S)],
        ["Total Anual", "", "", f_int(total_horas_mod), f_mon(importe_total_mod)]
    ]

    cedulas['7_mod'] = {
        'tabla': tabla_mod,
        'headers': headers_mod,
        'total_horas_mod': total_horas_mod,
        'importe_total_mod': importe_total_mod
    }
    return cedulas

def calcular_cedula_8_gif(d, cedulas):
    g = d['gif']
    
    total_manto = g['manto_1S'] + g['manto_2S']
    total_energeticos = g['energeticos_1S'] + g['energeticos_2S']
    
    tabla_gif = [
        ["Depreciación", f_mon(g['depreciacion'])],
        ["Seguros", f_mon(g['seguros'])],
        ["Mantenimiento (Total)", f_mon(total_manto)],
        ["Energéticos (Total)", f_mon(total_energeticos)],
        ["Varios", f_mon(g['varios'])]
    ]
    
    total_gif = g['depreciacion'] + g['seguros'] + total_manto + total_energeticos + g['varios']
    tabla_gif.append(["Total GIF", f_mon(total_gif)])
    
    gif_efectivo = total_gif - g['depreciacion']
    
    cedulas['8_gif'] = {
        'tabla': tabla_gif,
        'headers': ["Concepto", "Importe Anual"],
        'total_gif': total_gif,
        'gif_efectivo': gif_efectivo,
        'depreciacion_gif': g['depreciacion']
    }
    return cedulas

def calcular_cedula_9_gav(d, cedulas):
    ga = d['gav']
    total_ventas_2016 = cedulas['1_ventas']['total_ventas_2016']
    
    comisiones = total_ventas_2016 * ga['comisiones_tasa']
    total_varios = ga['varios_1S'] + ga['varios_2S']
    
    tabla_gav = [
        ["Depreciación", f_mon(ga['depreciacion'])],
        ["Sueldos y Salarios", f_mon(ga['sueldos'])],
        ["Comisiones", f_mon(comisiones)],
        ["Varios (Total)", f_mon(total_varios)],
        ["Intereses por Préstamo", f_mon(ga['intereses'])]
    ]
    
    total_gav = ga['depreciacion'] + ga['sueldos'] + comisiones + total_varios + ga['intereses']
    tabla_gav.append(["Total GAV", f_mon(total_gav)])
    
    gav_efectivo = total_gav - ga['depreciacion']
    
    cedulas['9_gav'] = {
        'tabla': tabla_gav,
        'headers': ["Concepto", "Importe Anual"],
        'total_gav': total_gav,
        'gav_efectivo': gav_efectivo,
        'depreciacion_gav': ga['depreciacion']
    }
    return cedulas

def calcular_cedula_10_costo_unitario(d, cedulas):
    u = d['uso_materiales']
    i = d['inventarios']
    m = d['mod']
    
    total_gif = cedulas['8_gif']['total_gif']
    
    base_gif_horas = cedulas['7_mod']['total_horas_mod']
    
    tasa_gif_hr = total_gif / base_gif_horas if base_gif_horas > 0 else 0
    
    costo_mp_A_2S = i['costo_mat_A_2S']
    costo_mp_B_2S = i['costo_mat_B_2S']
    costo_mp_C_2S = i['costo_mat_C_2S']
    costo_mod_2S = m['tarifa_hr_2S']

    costo_mp_xs = (u['XS_mat_A'] * costo_mp_A_2S) + (u['XS_mat_B'] * costo_mp_B_2S) + (u['XS_mat_C'] * costo_mp_C_2S)
    costo_mp_x = (u['X_mat_A'] * costo_mp_A_2S) + (u['X_mat_B'] * costo_mp_B_2S) + (u['X_mat_C'] * costo_mp_C_2S)
    costo_mp_xl = (u['XL_mat_A'] * costo_mp_A_2S) + (u['XL_mat_B'] * costo_mp_B_2S) + (u['XL_mat_C'] * costo_mp_C_2S)
    
    costo_mod_xs = m['XS_horas'] * costo_mod_2S
    costo_mod_x = m['X_horas'] * costo_mod_2S
    costo_mod_xl = m['XL_horas'] * costo_mod_2S
    
    costo_gif_xs = m['XS_horas'] * tasa_gif_hr
    costo_gif_x = m['X_horas'] * tasa_gif_hr
    costo_gif_xl = m['XL_horas'] * tasa_gif_hr
            
    cu_xs = costo_mp_xs + costo_mod_xs + costo_gif_xs
    cu_x = costo_mp_x + costo_mod_x + costo_gif_x
    cu_xl = costo_mp_xl + costo_mod_xl + costo_gif_xl
            
    headers_cu = [
        "Concepto",
        "Materiales (Costo 2S)",
        "Mano de Obra (Costo 2S)",
        "Gastos Ind.",
        "Costo Unitario"
    ]
    
    tabla_cu = [
        ["XS", f_mon(costo_mp_xs), f_mon(costo_mod_xs), f_mon(costo_gif_xs), f_mon(cu_xs)],
        ["X", f_mon(costo_mp_x), f_mon(costo_mod_x), f_mon(costo_gif_x), f_mon(cu_x)],
        ["XL", f_mon(costo_mp_xl), f_mon(costo_mod_xl), f_mon(costo_gif_xl), f_mon(cu_xl)]
    ]
    
    cedulas['10_costo_unitario'] = {
        'tabla': tabla_cu,
        'headers': headers_cu,
        'tasa_gif_hr': tasa_gif_hr,
        'base_gif_horas_supuesto': base_gif_horas,
        'cu_xs': cu_xs, 'cu_x': cu_x, 'cu_xl': cu_xl
    }
    return cedulas

def calcular_cedula_11_inv_finales(d, cedulas):
    i = d['inventarios']
    cu = cedulas['10_costo_unitario']
    c5 = cedulas['5_compras']
    
    costo_inv_final_mat_A = i['mat_A_final_u'] * c5['costo_inv_final_A']
    costo_inv_final_mat_B = i['mat_B_final_u'] * c5['costo_inv_final_B']
    costo_inv_final_mat_C = i['mat_C_final_u'] * c5['costo_inv_final_C']
    total_inv_final_mp = costo_inv_final_mat_A + costo_inv_final_mat_B + costo_inv_final_mat_C
    
    headers_mp = ["Concepto", "Unidades", "Costo Unitario (2S)", "Total"]
    tabla_inv_mp = [
        ["Material A", f_int(i['mat_A_final_u']), f_mon(c5['costo_inv_final_A']), f_mon(costo_inv_final_mat_A)],
        ["Material B", f_int(i['mat_B_final_u']), f_mon(c5['costo_inv_final_B']), f_mon(costo_inv_final_mat_B)],
        ["Material C", f_int(i['mat_C_final_u']), f_mon(c5['costo_inv_final_C']), f_mon(costo_inv_final_mat_C)],
        ["Total Inv. Final Materiales", "", "", f_mon(total_inv_final_mp)]
    ]

    costo_inv_final_pt_xs = i['pt_XS_final_u'] * cu['cu_xs']
    costo_inv_final_pt_x = i['pt_X_final_u'] * cu['cu_x']
    costo_inv_final_pt_xl = i['pt_XL_final_u'] * cu['cu_xl']
    total_inv_final_pt = costo_inv_final_pt_xs + costo_inv_final_pt_x + costo_inv_final_pt_xl
    
    headers_pt = ["Concepto", "Unidades", "Costo Unitario", "Total"]
    tabla_inv_pt = [
        ["Producto XS", f_int(i['pt_XS_final_u']), f_mon(cu['cu_xs']), f_mon(costo_inv_final_pt_xs)],
        ["Producto X", f_int(i['pt_X_final_u']), f_mon(cu['cu_x']), f_mon(costo_inv_final_pt_x)],
        ["Producto XL", f_int(i['pt_XL_final_u']), f_mon(cu['cu_xl']), f_mon(costo_inv_final_pt_xl)],
        ["Total Inv. Final Prod. Term.", "", "", f_mon(total_inv_final_pt)]
    ]
    
    cedulas['11_inv_finales'] = {
        'tabla_inv_mp': tabla_inv_mp,
        'headers_mp': headers_mp,
        'total_inv_final_mp': total_inv_final_mp,
        'tabla_inv_pt': tabla_inv_pt,
        'headers_pt': headers_pt,
        'total_inv_final_pt': total_inv_final_pt
    }
    return cedulas

def calcular_cedula_12_costo_prod_venta(d, cedulas):
    b15 = d['balance_2015']
    total_compras = cedulas['5_compras']['total_compras']
    total_inv_final_mp = cedulas['11_inv_finales']['total_inv_final_mp']
    importe_total_mod = cedulas['7_mod']['importe_total_mod']
    total_gif = cedulas['8_gif']['total_gif']
    total_inv_final_pt = cedulas['11_inv_finales']['total_inv_final_pt']
    
    inv_inicial_mp = b15['inv_materiales_costo']
    materiales_disponibles = inv_inicial_mp + total_compras
    materiales_utilizados = materiales_disponibles - total_inv_final_mp
    
    costo_produccion = materiales_utilizados + importe_total_mod + total_gif
    
    inv_inicial_pt = b15['inv_prod_terminado_costo']
    prod_terminado_disponible = costo_produccion + inv_inicial_pt
    costo_ventas = prod_terminado_disponible - total_inv_final_pt
    
    headers_costo = ["Concepto", "Importe", "Total"]
    tabla_costo = [
        ["(+) Inv. Inicial de Materiales", "", f_mon(inv_inicial_mp)],
        ["(+) Compras", "", f_mon(total_compras)],
        ["(=) Materiales Disponibles", "", f_mon(materiales_disponibles)],
        ["(-) Inv. Final de Materiales", "", f"({f_mon(total_inv_final_mp)})"],
        ["(=) Materiales Utilizados", "", f_mon(materiales_utilizados)],
        ["(+) Mano de Obra Directa", "", f_mon(importe_total_mod)],
        ["(+) Gastos Ind. de Fabricación", "", f_mon(total_gif)],
        ["(=) Costo de Producción", "", f_mon(costo_produccion)],
        ["(+) Inv. Inicial de Prod. Term.", "", f_mon(inv_inicial_pt)],
        ["(=) Prod. Terminado Disponible", "", f_mon(prod_terminado_disponible)],
        ["(-) Inv. Final de Prod. Term.", "", f"({f_mon(total_inv_final_pt)})"],
        ["(=) COSTO DE VENTAS", "", f_mon(costo_ventas)]
    ]
    
    cedulas['12_costo_prod_venta'] = {
        'tabla': tabla_costo,
        'headers': headers_costo,
        'costo_ventas': costo_ventas
    }
    return cedulas

def calcular_cedula_13_estado_resultados(d, cedulas):
    total_ventas_2016 = cedulas['1_ventas']['total_ventas_2016']
    costo_ventas = cedulas['12_costo_prod_venta']['costo_ventas']
    total_gav = cedulas['9_gav']['total_gav']
    tasa_isr_ptu = d['politicas']['tasa_isr_ptu']
    
    utilidad_bruta = total_ventas_2016 - costo_ventas
    utilidad_operacion = utilidad_bruta - total_gav
    
    impuestos = utilidad_operacion * tasa_isr_ptu if utilidad_operacion > 0 else 0
    utilidad_neta = utilidad_operacion - impuestos
    
    headers_er = ["Concepto", "Importe", "Total"]
    tabla_er = [
        ["Ventas", "", f_mon(total_ventas_2016)],
        ["(-) Costo de Ventas", "", f"({f_mon(costo_ventas)})"],
        ["(=) Utilidad Bruta", "", f_mon(utilidad_bruta)],
        ["(-) Gastos de Operación (GAV)", "", f"({f_mon(total_gav)})"],
        ["(=) Utilidad de Operación", "", f_mon(utilidad_operacion)],
        [f"(-) ISR y PTU ({tasa_isr_ptu * 100:.0f}%)", "", f"({f_mon(impuestos)})"],
        ["(=) UTILIDAD NETA", "", f_mon(utilidad_neta)]
    ]
    
    cedulas['13_estado_resultados'] = {
        'tabla': tabla_er,
        'headers': headers_er,
        'utilidad_neta': utilidad_neta,
        'impuestos_por_pagar': impuestos
    }
    return cedulas

def calcular_cedula_14_flujo_efectivo(d, cedulas):
    b15 = d['balance_2015']
    pol = d['politicas']
    
    total_entradas = cedulas['2_cobranza']['total_entradas']
    efectivo_disponible = b15['efectivo'] + total_entradas
    
    pago_proveedores_total = cedulas['6_proveedores']['pago_proveedores_total']
    pago_mod = cedulas['7_mod']['importe_total_mod']
    pago_gif = cedulas['8_gif']['gif_efectivo']
    pago_gav = cedulas['9_gav']['gav_efectivo']
    pago_isr_2015 = b15['isr_por_pagar']
    compra_activo_fijo = pol['compra_activo_fijo']
    
    total_salidas = (
        pago_proveedores_total + pago_mod + pago_gif + 
        pago_gav + pago_isr_2015 + compra_activo_fijo
    )
    
    flujo_efectivo_final = efectivo_disponible - total_salidas
    
    headers_fe = ["Concepto", "Importe", "Total"]
    tabla_fe = [
        ["Saldo Inicial de Efectivo", "", f_mon(b15['efectivo'])],
        ["(+) Entradas de Operación", f_mon(total_entradas), ""],
        ["(=) Efectivo Disponible", "", f_mon(efectivo_disponible)],
        ["(-) Salidas de Operación", "", ""],
        ["    Pago a Proveedores", f_mon(pago_proveedores_total), ""],
        ["    Pago Mano de Obra", f_mon(pago_mod), ""],
        ["    Pago GIF", f_mon(pago_gif), ""],
        ["    Pago GAV", f_mon(pago_gav), ""],
        ["    Pago ISR 2015", f_mon(pago_isr_2015), ""],
        ["    Compra de Activo Fijo", f_mon(compra_activo_fijo), ""],
        ["(=) Total de Salidas", "", f"({f_mon(total_salidas)})"],
        ["(=) FLUJO DE EFECTIVO FINAL", "", f_mon(flujo_efectivo_final)]
    ]
    
    cedulas['14_flujo_efectivo'] = {
        'tabla': tabla_fe,
        'headers': headers_fe,
        'flujo_efectivo_final': flujo_efectivo_final
    }
    return cedulas

def calcular_cedula_15_balance_general(d, cedulas):
    b15 = d['balance_2015']
    pol = d['politicas']
    
    efectivo_final = cedulas['14_flujo_efectivo']['flujo_efectivo_final']
    clientes_final = cedulas['2_cobranza']['saldo_clientes_final']
    inv_mp_final = cedulas['11_inv_finales']['total_inv_final_mp']
    inv_pt_final = cedulas['11_inv_finales']['total_inv_final_pt']
    
    total_activo_circulante = (
        efectivo_final + clientes_final + inv_mp_final + inv_pt_final +
        b15['deudores_diversos'] + b15['funcionarios_empleados']
    )
    
    depreciacion_total_2016 = cedulas['8_gif']['depreciacion_gif'] + cedulas['9_gav']['depreciacion_gav']
    dep_acumulada_final = b15['dep_acumulada'] + depreciacion_total_2016
    
    planta_equipo_bruto_final = b15['planta_equipo_bruto'] + pol['compra_activo_fijo']
    planta_equipo_neto = planta_equipo_bruto_final - dep_acumulada_final
    total_activo_no_circulante = b15['terreno'] + planta_equipo_neto
    
    total_activo = total_activo_circulante + total_activo_no_circulante
    
    proveedores_final = cedulas['6_proveedores']['saldo_proveedores_final']
    impuestos_por_pagar = cedulas['13_estado_resultados']['impuestos_por_pagar']
    
    total_pasivo_corto_plazo = proveedores_final + b15['documentos_por_pagar'] + impuestos_por_pagar
    
    total_pasivo_largo_plazo = b15['prestamos_bancarios_lp']
    
    total_pasivo = total_pasivo_corto_plazo + total_pasivo_largo_plazo
    
    utilidad_neta = cedulas['13_estado_resultados']['utilidad_neta']
    capital_ganado_final = b15['capital_ganado'] + utilidad_neta
    total_capital_contable = b15['capital_contribuido'] + capital_ganado_final
    
    total_pasivo_capital = total_pasivo + total_capital_contable
    
    tabla_bg = [
        ["ACTIVO", "PASIVO"],
        ["Activo Circulante", "Pasivo a Corto Plazo"],
        [f"  Efectivo", f_mon(efectivo_final), f"  Proveedores", f_mon(proveedores_final)],
        [f"  Clientes", f_mon(clientes_final), f"  Documentos por Pagar", f_mon(b15['documentos_por_pagar'])],
        [f"  Deudores Diversos", f_mon(b15['deudores_diversos']), f"  ISR y PTU por Pagar", f_mon(impuestos_por_pagar)],
        [f"  Funcionarios y Empleados", f_mon(b15['funcionarios_empleados']), f"Total Pasivo a Corto Plazo", f_mon(total_pasivo_corto_plazo)],
        [f"  Inventario de Materiales", f_mon(inv_mp_final), "", ""],
        [f"  Inventario de Prod. Term.", f_mon(inv_pt_final), "", ""],
        [f"Total Activo Circulante", f_mon(total_activo_circulante), "Pasivo a Largo Plazo", ""],
        ["", "", f"  Préstamos Bancarios LP", f_mon(total_pasivo_largo_plazo)],
        ["Activo No Circulante", "", f"Total Pasivo a Largo Plazo", f_mon(total_pasivo_largo_plazo)],
        [f"  Terreno", f_mon(b15['terreno']), "", ""],
        [f"  Planta y Equipo (Neto)", f_mon(planta_equipo_neto), "TOTAL PASIVO", f_mon(total_pasivo)],
        [f"    Bruto", f_mon(planta_equipo_bruto_final), "", ""],
        [f"    Dep. Acumulada", f"({f_mon(dep_acumulada_final)})", "", ""],
        [f"Total Activo No Circulante", f_mon(total_activo_no_circulante), "TOTAL PASIVO", f_mon(total_pasivo)],
        ["", "", "", ""],
        ["", "", "CAPITAL CONTABLE", ""],
        ["", "", f"  Capital Contribuido", f_mon(b15['capital_contribuido'])],
        ["", "", f"  Capital Ganado", f_mon(capital_ganado_final)],
        ["", "", f"    Capital Ganado (Inicial)", f_mon(b15['capital_ganado'])],
        ["", "", f"    Utilidad del Ejercicio", f_mon(utilidad_neta)],
        ["", "", f"Total Capital Contable", f_mon(total_capital_contable)],
        ["", "", "", ""],
        ["TOTAL ACTIVO", f_mon(total_activo), "TOTAL PASIVO + CAPITAL", f_mon(total_pasivo_capital)]
    ]

    headers_bg = ["", "Importe", "", "Importe"]
    
    cedulas['15_balance_general'] = {
        'tabla': tabla_bg,
        'headers': headers_bg,
        'total_activo': total_activo,
        'total_pasivo_capital': total_pasivo_capital
    }
    return cedulas

def calcular_cedulas_presupuestarias(d):
    if d is None:
        return None
    
    cedulas = {}
    
    try:
        calcular_cedula_1_ventas(d, cedulas)
        calcular_cedula_2_cobranza(d, cedulas)
        calcular_cedula_3_produccion(d, cedulas)
        calcular_cedula_4_req_materiales(d, cedulas)
        calcular_cedula_5_compras(d, cedulas)
        calcular_cedula_6_proveedores(d, cedulas)
        calcular_cedula_7_mod(d, cedulas)
        calcular_cedula_8_gif(d, cedulas)
        calcular_cedula_9_gav(d, cedulas)
        calcular_cedula_10_costo_unitario(d, cedulas)
        calcular_cedula_11_inv_finales(d, cedulas)
        calcular_cedula_12_costo_prod_venta(d, cedulas)
        calcular_cedula_13_estado_resultados(d, cedulas)
        calcular_cedula_14_flujo_efectivo(d, cedulas)
        calcular_cedula_15_balance_general(d, cedulas)
    except Exception as e:
        print(f"\n!!! ERROR DURANTE EL CÁLCULO DE CÉDULAS: {e}")
        print("Esto puede deberse a un formato inesperado en los datos.")
        import traceback
        traceback.print_exc()
        return None
        
    print(">>> Cédulas calculadas exitosamente.")
    return cedulas

def mostrar_menu(cedulas):
    if cedulas is None:
        print("No hay cédulas para mostrar. Saliendo.")
        return
        
    tablefmt_style = "rounded_outline"

    while True:
        print("\n--- MENÚ DE CÉDULAS PRESUPUESTARIAS ---")
        print(" 1. Presupuesto de Ventas")
        print(" 2. Determinación del saldo de Clientes y Flujo de Entradas")
        print(" 3. Presupuesto de Producción")
        print(" 4. Presupuesto de Requerimiento de Materiales")
        print(" 5. Presupuesto de Compra de Materiales")
        print(" 6. Determinación del Saldo de Proveedores y Flujo de Salidas")
        print(" 7. Presupuesto de Mano de Obra Directa")
        print(" 8. Presupuesto de Gastos Indirectos de Fabricación")
        print(" 9. Presupuesto de Gastos de Operación")
        print("10. Determinación del Costo Unitario de Productos Terminados")
        print("11. Valuación de Inventarios Finales")
        print("12. Estado de Costo de Producción y Venta")
        print("13. Estado de Resultados")
        print("14. Estado de Flujo de Efectivo")
        print("15. Balance General")
        print(" Q. Salir")
        
        opcion = input("Selecciona una opción: ").strip().lower()
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        if opcion == '1':
            print("\n--- 1. Presupuesto de Ventas ---")
            tabla = cedulas['1_ventas']['tabla']
            headers = cedulas['1_ventas']['headers']
            print(tabulate(tabla, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))

        elif opcion == '2':
            print("\n--- 2. Determinación del saldo de Clientes y Flujo de Entradas ---")
            headers = cedulas['2_cobranza']['headers']
            
            print("\nDeterminación del Saldo de Clientes")
            tabla_saldo = cedulas['2_cobranza']['tabla_saldo_clientes']
            print(tabulate(tabla_saldo, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))

            print("\nDeterminación del Flujo de Entradas")
            tabla_flujo = cedulas['2_cobranza']['tabla_flujo_entradas']
            print(tabulate(tabla_flujo, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))

        elif opcion == '3':
            print("\n--- 3. Presupuesto de Producción ---")
            df = cedulas['3_produccion']['dataframe']
            print(tabulate(df, headers='keys', tablefmt=tablefmt_style, floatfmt=",.0f"))
            
        elif opcion == '4':
            print("\n--- 4. Presupuesto de Requerimiento de Materiales ---")
            tabla = cedulas['4_req_materiales']['tabla']
            headers = cedulas['4_req_materiales']['headers']
            print(tabulate(tabla, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))

        elif opcion == '5':
            print("\n--- 5. Presupuesto de Compra de Materiales ---")
            tabla = cedulas['5_compras']['tabla']
            headers = cedulas['5_compras']['headers']
            print(tabulate(tabla, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))
            print(f"\nTotal Compras (Importe): ${cedulas['5_compras']['total_compras']:,.2f}")
        
        elif opcion == '6':
            print("\n--- 6. Determinación del Saldo de Proveedores y Flujo de Salidas ---")
            headers = cedulas['6_proveedores']['headers']
            
            print("\nDeterminación del Saldo de Proveedores")
            tabla_saldo = cedulas['6_proveedores']['tabla_saldo_prov']
            print(tabulate(tabla_saldo, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))

            print("\nDeterminación del Flujo de Salidas (Pago a Proveedores)")
            tabla_flujo = cedulas['6_proveedores']['tabla_flujo_salidas']
            print(tabulate(tabla_flujo, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))

        elif opcion == '7':
            print("\n--- 7. Presupuesto de Mano de Obra Directa ---")
            tabla = cedulas['7_mod']['tabla']
            headers = cedulas['7_mod']['headers']
            print(tabulate(tabla, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))

        elif opcion == '8':
            print("\n--- 8. Presupuesto de Gastos Indirectos de Fabricación ---")
            tabla = cedulas['8_gif']['tabla']
            headers = cedulas['8_gif']['headers']
            print(tabulate(tabla, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))
            
        elif opcion == '9':
            print("\n--- 9. Presupuesto de Gastos de Operación ---")
            tabla = cedulas['9_gav']['tabla']
            headers = cedulas['9_gav']['headers']
            print(tabulate(tabla, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))

        elif opcion == '10':
            print("\n--- 10. Determinación del Costo Unitario de Productos Terminados ---")
            tabla = cedulas['10_costo_unitario']['tabla']
            headers = cedulas['10_costo_unitario']['headers']
            print(tabulate(tabla, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))
            print(f"\n(SUPUESTO) Base GIF aplicada: {cedulas['10_costo_unitario']['base_gif_horas_supuesto']:,.0f} Horas MOD")
            print(f"Tasa GIF resultante: ${cedulas['10_costo_unitario']['tasa_gif_hr']:.2f} por Hora MOD")

        elif opcion == '11':
            print("\n--- 11. Valuación de Inventarios Finales ---")
            print("\nInventario Final de Materiales (Valuado a Costo 2S)")
            tabla_mp = cedulas['11_inv_finales']['tabla_inv_mp']
            headers_mp = cedulas['11_inv_finales']['headers_mp']
            print(tabulate(tabla_mp, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))
            
            print("\nInventario Final de Producto Terminado")
            tabla_pt = cedulas['11_inv_finales']['tabla_inv_pt']
            headers_pt = cedulas['11_inv_finales']['headers_pt']
            print(tabulate(tabla_pt, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))

        elif opcion == '12':
            print("\n--- 12. Estado de Costo de Producción y Venta ---")
            tabla = cedulas['12_costo_prod_venta']['tabla']
            headers = cedulas['12_costo_prod_venta']['headers']
            print(tabulate(tabla, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))

        elif opcion == '13':
            print("\n--- 13. Estado de Resultados ---")
            tabla = cedulas['13_estado_resultados']['tabla']
            headers = cedulas['13_estado_resultados']['headers']
            print(tabulate(tabla, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))

        elif opcion == '14':
            print("\n--- 14. Estado de Flujo de Efectivo ---")
            tabla = cedulas['14_flujo_efectivo']['tabla']
            headers = cedulas['14_flujo_efectivo']['headers']
            print(tabulate(tabla, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))

        elif opcion == '15':
            print("\n--- 15. Balance General ---")
            tabla = cedulas['15_balance_general']['tabla']
            headers = cedulas['15_balance_general']['headers']
            print(tabulate(tabla, headers=headers, tablefmt=tablefmt_style, stralign="left", numalign="right"))
            
            activo_num = cedulas['15_balance_general']['total_activo']
            pasivo_cap_num = cedulas['15_balance_general']['total_pasivo_capital']
            activo = f_mon(activo_num)
            pasivo_cap = f_mon(pasivo_cap_num)

            print(f"\nChequeo: Activo ({activo}) vs Pasivo+Capital ({pasivo_cap})")
            if abs(activo_num - pasivo_cap_num) > 0.01: 
                print(f">>> ¡ALERTA! El Balance General no cuadra por: {f_mon(abs(activo_num - pasivo_cap_num))}")
            else:
                print(">>> ¡Balance Cuadrado!")


        elif opcion == 'q':
            print("Saliendo del programa...")
            break
            
        else:
            print("Opción no válida. Inténtalo de nuevo.")
        
        input("\nPresiona Enter para continuar...")
        os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_datos_constantes():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- Calculadora de Presupuesto Maestro ---")
    print("\nLos siguientes datos están precargados y se usarán como constantes:")
    
    tablefmt_style = "rounded_outline"
    
    print("\nBalance General al 31 de Diciembre del 2015")
    balance_data = [
        ["Efectivo", f_mon(200000.0), "Proveedores", f_mon(75000.0)],
        ["Clientes", f_mon(90000.0), "Documentos por Pagar", f_mon(800000.0)],
        ["Deudores Diversos", f_mon(15000.0), "ISR Por Pagar", f_mon(40000.0)],
        ["Funcionarios y Empleados", f_mon(5000.0), "Préstamos Bancarios LP", f_mon(1000000.0)],
        ["Inventario de Materiales", f_mon(65000.0), "Capital Contribuido", f_mon(1000000.0)],
        ["Inventario de Prod. Terminado", f_mon(180000.0), "Capital Ganado", f_mon(640000.0)],
        ["Terreno", f_mon(1500000.0), "", ""],
        ["Planta y Equipo (Bruto)", f_mon(2200000.0), "", ""],
        ["Depreciación Acumulada", f"({f_mon(700000.0)})", "", ""],
    ]
    print(tabulate(balance_data, headers=["Activos", "Importe", "Pasivo y Capital", "Importe"], tablefmt=tablefmt_style, stralign="left", numalign="right"))

    print("\nPolíticas Constantes de la Empresa")
    politicas_data = [
        ["Tasa ISR", "30.0%"],
        ["Tasa PTU", "10.0%"],
        ["Tasa Impuestos Total", "40.0%"],
        ["Cobranza Ventas 2016 (Contado)", "75.0%"],
        ["Pago Compras 2016 (Contado)", "60.0%"],
        ["Compra de Activo Fijo (Maquinaria)", f_mon(110000.0)],
    ]
    print(tabulate(politicas_data, headers=["Concepto", "Valor"], tablefmt=tablefmt_style, stralign="left", numalign="right"))
    
    input("\nPresiona Enter para iniciar la captura de datos...")
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    mostrar_datos_constantes()

    print("Por favor, introduce los datos para el presupuesto de 2016.")
    datos_usuario = pedir_datos_usuario()
    
    if datos_usuario:
        print("\nCalculando todas las cédulas...")
        cedulas_calculadas = calcular_cedulas_presupuestarias(datos_usuario)
        
        if cedulas_calculadas:
            print("¡Cálculo completado!")
            input("Presiona Enter para mostrar el menú...")
            os.system('cls' if os.name == 'nt' else 'clear')
            mostrar_menu(cedulas_calculadas)
        else:
            print("No se pudieron calcular las cédulas. Saliendo.")
    else:
        print("No se pudieron cargar los datos.")

if __name__ == "__main__":
    main()