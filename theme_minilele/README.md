# Theme Mini Lele Boutique — Odoo 19

Tema oficial de [Mini Lele Boutique](https://www.minilele.boutique) para Odoo 19. Aplica el design system de la boutique (paleta candy, acentos dorados, tipografías redondeadas) al sitio web y al eCommerce.

---

## ¿Qué incluye?

| Pieza | Qué hace |
|---|---|
| **Paleta de colores** | Preset `minilele` con candy + dorado + crema, seleccionado por default al instalar |
| **Tipografías** | Fredoka (display) + Nunito (body) + Pacifico (script) desde Google Fonts |
| **Bootstrap overrides** | Botones pill, cards radius 24px, inputs con focus rosa |
| **Header translúcido** | Sticky con backdrop-blur, logo de 56px, nav con underline rosa |
| **Footer cream con dividers dorados** | Cards de footer con headings en dorado oscuro |
| **8 snippets de boutique** | Hero, Categorías, Beneficios (banda dorada), Productos, Historia, Testimonios, Lookbook Instagram, Newsletter |
| **eCommerce (`website_sale`)** | Tarjetas de producto, precio, "agregar al carrito" — todos con look candy gloss |

---

## Instalación (self-hosted con Docker o servidor propio)

### 1. Copia el módulo a tu folder de addons

```bash
# Si tienes una carpeta de addons custom (recomendado)
cp -r theme_minilele /path/to/your/odoo/custom-addons/

### 2. Reinicia Odoo y actualiza la lista de Apps

```bash
sudo systemctl restart odoo
```


---

## Personalización

### Cambiar colores

Editar `static/src/scss/primary_variables.scss`. Las variables al inicio del archivo son las que controlan toda la paleta:

```scss
$minilele-candy-pink:    #F06AAA;   // ← cambia esto y se actualiza el sitio entero
$minilele-gold-500:      #E5B554;
// ...
```

Luego: **Apps → Mini Lele → Upgrade**.

### Cambiar las tipografías

En el website builder: **Customize → Theme Options → Font** — elige cualquiera de las 3 registradas o agrega una nueva en `primary_variables.scss`:

```scss
$o-theme-font-configs-custom: (
    'Mi Font': ( 'family': ('Mi Font', sans-serif), 'url': 'Mi+Font:400,700' ),
    // ...
);
```

### Agregar más snippets a la página

Modo edición → barra lateral derecha → busca "Mini Lele" → arrastra a la página.

---

## Estructura del módulo

```
theme_minilele/
├── __init__.py                              # vacío
├── __manifest__.py                          # metadata, depends, data, assets
├── README.md                                # este archivo
│
├── views/
│   ├── layout.xml                           # Header top strip, footer copyright
│   ├── snippets_register.xml                # Registra snippets en el builder
│   └── snippets/
│       ├── s_minilele_hero.xml
│       ├── s_minilele_categories.xml
│       ├── s_minilele_promo_strip.xml
│       ├── s_minilele_products.xml
│       ├── s_minilele_story.xml
│       ├── s_minilele_testimonials.xml
│       ├── s_minilele_lookbook.xml
│       └── s_minilele_newsletter.xml
│
└── static/
    ├── description/
    │   ├── index.html                       # Apps store listing
    │   ├── icon.png                         # Icono en Apps
    │   └── cover.png                        # Cover para Apps
    └── src/
        ├── scss/
        │   ├── primary_variables.scss       # Paleta + tipografías + Bootstrap overrides
        │   ├── fonts.scss                   # Google Fonts @import
        │   ├── theme.scss                   # Estilos base (header, footer, botones)
        │   └── snippets.scss                # Estilos de los 8 snippets
        ├── img/
        │   ├── logo.png                     # Logo de Mini Lele
        │   └── snippets/                    # Thumbnails que aparecen en el builder
        │       └── *.svg
```

---

## eCommerce — pasos siguientes

El tema ya estiliza `website_sale` (tarjetas, botón comprar, precios) pero **no crea productos**. Para tener un shop funcionando:

1. **Crea las categorías de producto** que usamos en los snippets: `Niñas`, `Niños`, `Bebé`, `Bautizo`. En Odoo: *Sales → Products → Product Categories* o *Website → eCommerce → Product Categories*.
2. **Crea productos** con foto, precio y stock. *Website → eCommerce → Products → New*.
3. **Reemplaza el snippet "Productos" en la home** por el snippet nativo `Products` de Odoo (lo encuentras en el builder bajo "eCommerce") — ese sí carga productos reales de la base. El snippet `s_minilele_products` que viene en el tema es decorativo / editorial.
4. **Configura pagos**: *Website → Configuration → Payment Providers*. Para México: Stripe, Conekta, MercadoPago, OXXO via PayU.
5. **Configura envíos**: *Website → Configuration → Shipping Methods*.

---

## Compatibilidad

- ✅ Odoo 19 (versión target)
---

## Troubleshooting

**No veo el tema en Apps después de instalar**
→ Activa modo desarrollador, luego **Apps → Update Apps List**. Asegúrate de que el filtro "Apps" esté quitado del buscador.

**Veo el módulo pero los estilos no se aplican**
→ Reinicia Odoo con el flag  `-u theme_minilele` en línea de comando:
```bash
./odoo-bin -d tu_db -u theme_minilele
```

**Las tipografías no cargan**
→ El servidor del cliente bloquea Google Fonts? Descarga los `.woff2` y sírvelos localmente:
1. Mete los archivos en `static/src/fonts/`
2. Reemplaza `fonts.scss` con `@font-face { src: url('/theme_minilele/static/src/fonts/Fredoka.woff2') ... }`

---