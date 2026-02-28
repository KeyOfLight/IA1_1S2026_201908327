import tkinter as tk
from tkinter import font, messagebox, scrolledtext
from database import save_diagnosis, obtener_sintomas, obtener_diagnostico_prolog, obtener_recomendacion_prolog, es_condicion_urgente


class PatientDiagnosticModule:
    """Módulo de diagnóstico preliminar para pacientes (basado en Prolog)"""
    
    def __init__(self, window):
        self.window = window
        self.window.title("Módulo de Diagnóstico - Pacientes")
        self.window.geometry("900x700")
        self.window.resizable(False, False)
        
        # Obtener síntomas del motor de Prolog
        self.sintomas_disponibles = obtener_sintomas()
        
        # Si Prolog no está disponible, usar fallback
        if not self.sintomas_disponibles:
            print("⚠️  Prolog no disponible, usando síntomas de fallback")
            self.sintomas_disponibles = [
                "Fiebre", "Tos", "Dolor de cabeza", "Dolor de garganta",
                "Congestión nasal", "Diarrea", "Náuseas", "Fatiga",
                "Dolor abdominal", "Mareos"
            ]
        
        self.configure_styles()
        self.create_interface()
    
    def configure_styles(self):
        """Configura los estilos de fuentes"""
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.text_font = font.Font(family="Helvetica", size=10)
    
    def create_interface(self):
        """Crea la interfaz de diagnóstico"""
        main_frame = tk.Frame(self.window, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Encabezado
        header = tk.Frame(main_frame, bg="#27ae60")
        header.pack(fill=tk.X)
        
        title = tk.Label(
            header,
            text="Diagnóstico Preliminar",
            font=self.title_font,
            fg="white",
            bg="#27ae60",
            pady=15
        )
        title.pack()
        
        # Contenido principal
        content_frame = tk.Frame(main_frame, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Instrucciones
        instruction_label = tk.Label(
            content_frame,
            text="Seleccione sus síntomas del listado. Puede seleccionar múltiples síntomas:",
            font=self.subtitle_font,
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        instruction_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para síntomas con scrollbar
        symptoms_frame = tk.Frame(content_frame, bg="white", relief=tk.SUNKEN, bd=1)
        symptoms_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scrollbar = tk.Scrollbar(symptoms_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas = tk.Canvas(
            symptoms_frame,
            bg="white",
            yscrollcommand=scrollbar.set,
            highlightthickness=0
        )
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)
        
        # Frame interior para los checkbuttons
        inner_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")
        
        self.symptom_vars = {}
        # Usar síntomas del motor Prolog
        for symptom in sorted(self.sintomas_disponibles):
            var = tk.BooleanVar()
            self.symptom_vars[symptom] = var
            
            check = tk.Checkbutton(
                inner_frame,
                text=symptom,
                variable=var,
                font=self.text_font,
                bg="white",
                activebackground="#ecf0f1"
            )
            check.pack(anchor=tk.W, padx=10, pady=5)
        
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Botones de acción
        button_frame = tk.Frame(content_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=15)
        
        btn_diagnose = tk.Button(
            button_frame,
            text="Obtener Diagnóstico Preliminar",
            font=self.text_font,
            bg="#27ae60",
            fg="white",
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.generate_diagnosis
        )
        btn_diagnose.pack(side=tk.LEFT, padx=5)
        
        btn_clear = tk.Button(
            button_frame,
            text="Limpiar",
            font=self.text_font,
            bg="#95a5a6",
            fg="white",
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.clear_selection
        )
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        btn_close = tk.Button(
            button_frame,
            text="Cerrar",
            font=self.text_font,
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.window.destroy
        )
        btn_close.pack(side=tk.RIGHT, padx=5)
        
        # Aviso importante
        warning_label = tk.Label(
            content_frame,
            text="⚠ AVISO: Este diagnóstico es preliminar y educativo. No reemplaza la consulta médica profesional.",
            font=font.Font(family="Helvetica", size=9, weight="bold"),
            fg="white",
            bg="#e74c3c",
            wraplength=800,
            padx=10,
            pady=8
        )
        warning_label.pack(fill=tk.X)
    
    def generate_diagnosis(self):
        """Genera el diagnóstico preliminar usando el motor Prolog"""
        selected_symptoms = [sym for sym, var in self.symptom_vars.items() if var.get()]
        
        if not selected_symptoms:
            messagebox.showwarning("Aviso", "Por favor seleccione al menos un síntoma")
            return
        
        # Obtener diagnósticos del motor Prolog
        try:
            diagnosticos_prolog = obtener_diagnostico_prolog(selected_symptoms)
            if not diagnosticos_prolog:
                messagebox.showwarning("Aviso", "No se encontraron diagnósticos para los síntomas seleccionados")
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error al consultar Prolog: {str(e)}\n\nAsegúrese de tener SWI-Prolog instalado y pyswip configurado.")
            return
        
        # Crear ventana de resultados
        result_window = tk.Toplevel(self.window)
        result_window.title("Resultados del Diagnóstico Preliminar")
        result_window.geometry("700x600")
        result_window.resizable(False, False)
        
        # Encabezado
        header = tk.Frame(result_window, bg="#3498db")
        header.pack(fill=tk.X)
        
        title = tk.Label(
            header,
            text="Resultados del Diagnóstico (Motor Prolog)",
            font=self.title_font,
            fg="white",
            bg="#3498db",
            pady=15
        )
        title.pack()
        
        # Contenido
        content = tk.Frame(result_window, bg="#f0f0f0")
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Síntomas seleccionados
        symptom_title = tk.Label(
            content,
            text="Síntomas Reportados:",
            font=self.subtitle_font,
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        symptom_title.pack(anchor=tk.W)
        
        symptom_text = ", ".join(selected_symptoms)
        symptom_label = tk.Label(
            content,
            text=symptom_text,
            font=self.text_font,
            fg="#34495e",
            bg="#ecf0f1",
            wraplength=650,
            justify=tk.LEFT,
            padx=10,
            pady=8
        )
        symptom_label.pack(anchor=tk.W, fill=tk.X, pady=(5, 15))
        
        # Posibles condiciones (desde Prolog)
        condition_title = tk.Label(
            content,
            text="Posibles Condiciones de Salud (Motor Prolog - por relevancia):",
            font=self.subtitle_font,
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        condition_title.pack(anchor=tk.W)
        
        condition_text = tk.Text(content, height=10, width=80, font=self.text_font)
        condition_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Mostrar diagnósticos de Prolog con relevancia
        for i, (condition, score) in enumerate(diagnosticos_prolog, 1):
            relevance = "Alta" if score >= 2 else "Media"
            urgencia = " ⚠️ URGENTE" if es_condicion_urgente(condition) else ""
            recomendacion = obtener_recomendacion_prolog(condition)
            condition_text.insert(tk.END, f"{i}. {condition} (Relevancia: {relevance}){urgencia}\n")
        
        condition_text.config(state=tk.DISABLED)
        
        # Recomendación final
        recommendation_frame = tk.Frame(content, bg="#fff3cd", relief=tk.SUNKEN, bd=1)
        recommendation_frame.pack(fill=tk.X, pady=15)
        
        recommendation_text = """IMPORTANTE - RECOMENDACIÓN:

Este diagnóstico es PRELIMINAR y EDUCATIVO solamente. 
No debe ser utilizado como sustituto de la consulta médica profesional.

Por favor, diríjase a un médico calificado para:
• Confirmación del diagnóstico
• Evaluación clínica completa  
• Tratamiento médico apropiado
• Cualquier inquietud sobre su salud"""
        
        recommendation_label = tk.Label(
            recommendation_frame,
            text=recommendation_text,
            font=font.Font(family="Helvetica", size=9),
            fg="#856404",
            bg="#fff3cd",
            justify=tk.LEFT,
            padx=10,
            pady=10
        )
        recommendation_label.pack(anchor=tk.W)
        
        # Botones
        button_frame = tk.Frame(content, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=10)
        
        btn_save = tk.Button(
            button_frame,
            text="Guardar Registro",
            font=self.text_font,
            bg="#27ae60",
            fg="white",
            padx=10,
            py=8,
            cursor="hand2",
            command=lambda: self.save_diagnosis_record(selected_symptoms, diagnosticos_prolog)
        )
        btn_save.pack(side=tk.LEFT, padx=5)
        
        btn_close = tk.Button(
            button_frame,
            text="Cerrar",
            font=self.text_font,
            bg="#e74c3c",
            fg="white",
            padx=10,
            py=8,
            cursor="hand2",
            command=result_window.destroy
        )
        btn_close.pack(side=tk.RIGHT, padx=5)
    
    def save_diagnosis_record(self, symptoms, conditions):
        """Guarda el registro del diagnóstico (datos de Prolog)"""
        save_diagnosis(symptoms, conditions)
        messagebox.showinfo("Éxito", "El registro ha sido guardado exitosamente\n(Procesado por motor Prolog)")
    
    def clear_selection(self):
        """Limpia la selección de síntomas"""
        for var in self.symptom_vars.values():
            var.set(False)
