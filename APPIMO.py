# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 22:01:19 2024

@author: hugod
"""
#Modif a apporter : Je veux une RP, j'ai une RP, je veux rester locataire. Je veux allouer autant de mon salaire en phase 0123 (mais comment comparer richesse?)
# SI achat RP, Loyer = Mensualité -> incidence capacité d'emprunt. 
import streamlit as st
from math import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



# st.markdown(
#     """
#     <style>
#     [data-testid="stSidebar"] {
#         background-color: #2E2E40;   /* couleur de fond */
#     }
#     [data-testid="stSidebar"] * {
#         color: white !important;     /* force le texte en blanc */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# st.markdown(
#     """
#     <style>
#     /* Fond de la sidebar */
#     [data-testid="stSidebar"] {
#         background-color: #2E2E10;
#     }

#     /* Labels / titres des widgets */
#     [data-testid="stSidebar"] label, 
#     [data-testid="stSidebar"] .css-1aumxhk { 
#         color: white !important; 
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )


st.title("ACHAT EN SERIE : MASTER VISION !")
with st.expander("Clique ici pour en savoir plus sur la lecture du graphique"):
    st.write("""**Cashflow** = Capacité d'épargne mensuel + revenu locatif - mensualité et charges  
➡️ *Cumul de ce que tu as en trop sur ton compte chaque fin du mois*

**Dette** = Solde restant dû  
➡️ *Ce que tu dois donner à la banque si tu vendais tes biens*

**Gain** = Part du bien que tu possèdes réellement + la somme de tes économies  
➡️ *L'héritage de tes enfanst* 

**Eco Fictive** = somme de ta capacité d'épargne initiale  
➡️ *Ce que tu aurais sur ton compte si tu n'avais pas investi*""")

st.sidebar.title("WELCOME")
with st.sidebar.expander("Clique ici pour en savoir plus sur le code"):
    st.markdown("""
Remplis tes données personnelles et les données des achats que tu souhaites faire.  Observe les résultats à droite.  

La simulation comptabilise ton épargne et tes garanties.  
Dès que les conditions sont réunies, le simulateur t'ajoute un bien à ton patrimoine.  

Commence avec un achat et essaye de jouer avec tous les paramètres pour comprendre leurs incidences.  
Essaye d'obtenir le meilleur résultat avec 1 achat, puis avec plusieurs achats ! 
""")

st.sidebar.title("NOMBRE D ACHATS")
choix = st.sidebar.radio(
    "NOMBRE D'ACQUISITION PROJETE :",
    ["1", "2", "3","4"],
    index=1,
    horizontal=True
)
nbbien = int(choix[0])
#nbbien=st.number_input("NOMBRE D ACHAT SOUHAITE", value=2, step=1)


st.sidebar.title("PERSO")
salaire=st.sidebar.number_input("SALAIRE", value=2700, step=100)







RAV=1500
# RAV=(salaire-capacite_epargne0)#Reste A Vivre
# st.sidebar.write(f"Reste a vivre: **{(RAV):,.0f} €/mois**")
#st.sidebar.write("Ce que tu as sur ton compte")
    # st.title("HUGO DE COSTER")
    # st.header("Profil")

epargne=st.sidebar.number_input("EPARGNE", value=5000, step=1000)
st.sidebar.title("ACHAT 1")

# --- Définition des presets ---
presets = {
    "Aucun": {},
    "Colloc 4ch sans travaux": {
        "prix": 200000,
        "travaux": 5000,
        "loyer": 1600,
        "charges": 200,
        "taux": 3.5,
        "duree": 25,
        "aprt": 20,
    },
    "Colloc 4ch avec travaux": {
        "prix": 100000,
        "travaux": 70000,
        "loyer": 1600,
        "charges": 200,
        "taux": 3.5,
        "duree": 25,
        "aprt": 20,
    }
}



# --- ACHAT 1 ---

with st.sidebar.expander("ACHAT 1", expanded=True):  # expanded=True si tu veux que ça s'ouvre par défaut

    preset1 = st.selectbox("Preset Achat 1 (remettre sur -aucun- apres sélection)", presets.keys(), key="preset1")

    if preset1 != "Aucun":
        for k, v in presets[preset1].items():
            st.session_state[f"{k}1"] = v

    capacite_epargne0 = st.number_input("1. PART DE SALAIRE DEDIE A L'investissement AVANT ACHAT 1", value=500, step=50)
    prix1 = st.slider("1. PRIX DU BIEN", min_value=0, max_value=500000, value=st.session_state.get("prix1", 100000), step=5000, key="prix1")
    travaux1 = st.slider("1. PRIX DES TRAVAUX", min_value=0, max_value=500000, value=st.session_state.get("travaux1", 80000), step=1000, key="travaux1")
    estimation1 = st.number_input("1. ESTIMATION DU BIEN", value=prix1+travaux1, step=5000)
    loyer1 = st.number_input("1. LOYER", value=st.session_state.get("loyer1", 1600), step=50, key="loyer1")
    charges1 = st.number_input("1. CHARGES", value=st.session_state.get("charges1", 200), step=50, key="charges1")
    taux1 = st.number_input("1. TAUX", value=st.session_state.get("taux1", 3.5), step=0.1, key="taux1")
    duree1 = st.number_input("1. DUREE DU CREDIT", value=st.session_state.get("duree1", 25), step=5, key="duree1")
    aprt1 = st.number_input("1. APPORT % du prix", value=st.session_state.get("aprt1", 0), step=5, key="aprt1")
    DrEn1 = float(st.radio("1. Droit d'enregistrement % :", ["3", "12.5"], index=0, horizontal=True)) + 2
    choix = st.selectbox("1. Sélectionne une hypothèque :", ["1.Hyp dispo (saisir valeur)", "1.Aucune hyp dispo"])
    hyp_dispo1 = st.number_input("1. Hyp Dispo", value=0, step=10000)
    apport1 = (aprt1*(prix1+travaux1)/100) + (prix1*DrEn1/100)


# --- ACHAT 2 ---
# Sidebar - ACHAT 2
with st.sidebar.expander("ACHAT 2", expanded=False):  # expanded=True si tu veux qu'il soit ouvert par défaut

    preset2 = st.selectbox("Preset Achat 2 (remettre sur -aucun- apres sélection)", presets.keys(), key="preset2")

    if preset2 != "Aucun":
        for k, v in presets[preset2].items():
            st.session_state[f"{k}2"] = v

    capacite_epargne1 = st.number_input("2. PART DE SALAIRE DEDIE AVANT ACHAT 2", value=400, step=50)
    prix2 = st.slider("2. PRIX DU BIEN", min_value=0, max_value=500000, value=st.session_state.get("prix2", 150000), step=5000, key="prix2")
    travaux2 = st.slider("2. PRIX DES TRAVAUX", min_value=0, max_value=500000, value=st.session_state.get("travaux2", 60000), step=1000, key="travaux2")
    estimation2 = st.number_input("2. ESTIMATION DU BIEN", value=prix2+travaux2, step=5000)
    loyer2 = st.number_input("2. LOYER", value=st.session_state.get("loyer2", 1600), step=50, key="loyer2")
    charges2 = st.number_input("2. HARGES", value=st.session_state.get("charges2", 200), step=50, key="charges2")
    taux2 = st.number_input("2. TAUX", value=st.session_state.get("taux2", 3.5), step=0.1, key="taux2")
    duree2 = st.number_input("2. DUREE DU CREDIT", value=st.session_state.get("duree2", 20), step=5, key="duree2")
    aprt2 = st.number_input("2. APPORT % du prix", value=st.session_state.get("aprt2", 0), step=5, key="aprt2")
    DrEn2 = float(st.radio("2. Droit d'enregistrement % :", ["3", "12.5"], index=1, horizontal=True)) + 2
    choix = st.selectbox("2. Sélectionne une hypothèque2 :", ["2. Hyp dispo (saisir valeur)", "2. Aucune hyp dispo", "2. Hypotequer bien1"])
    hyp_dispo2 = st.number_input("2. Hyp Dispo", value=0, step=5000)
    apport2 = (aprt2*(prix2+travaux2)/100) + (prix2*DrEn2/100)
# st.sidebar.title("ACHAT 2")



# --- ACHAT 3 ---

with st.sidebar.expander("ACHAT 3 ", expanded=False):  # False = replié par défaut

    preset3 = st.selectbox("Preset Achat 3 (remettre sur -aucun- apres sélection)", presets.keys(), key="preset3")

    if preset3 != "Aucun":
        for k, v in presets[preset3].items():
            st.session_state[f"{k}3"] = v

    capacite_epargne2 = st.number_input("3. PART DE SALAIRE DEDIE AVANT ACHAT", value=300, step=50)
    prix3 = st.slider("3. PRIX DU BIEN", min_value=0, max_value=500000, value=st.session_state.get("prix3", 150000), step=5000, key="prix3")
    travaux3 = st.slider("3. PRIX DES TRAVAUX", min_value=0, max_value=500000, value=st.session_state.get("travaux3", 60000), step=1000, key="travaux3")
    estimation3 = st.number_input("3. ESTIMATION DU BIEN", value=prix3+travaux3, step=5000)
    loyer3 = st.number_input("3. LOYER", value=st.session_state.get("loyer3", 1600), step=50, key="loyer3")
    charges3 = st.number_input("3. CHARGES", value=st.session_state.get("charges3", 200), step=50, key="charges3")
    taux3 = st.number_input("3. TAUX", value=st.session_state.get("taux3", 3.5), step=0.1, key="taux3")
    duree3 = st.number_input("3. DUREE DU CREDIT", value=st.session_state.get("duree3", 20), step=5, key="duree3")
    aprt3 = st.number_input("3. APPORT % du prix", value=st.session_state.get("aprt3", 20), step=5, key="aprt3")
    DrEn3 = float(st.radio("3. Droit d'enregistrement % :", ["3", "12.5"], index=1, horizontal=True)) + 2
    choix3 = st.selectbox("3. Sélectionne une hypothèque :", ["3. Hyp dispo (saisir valeur)", "3. Aucune hyp dispo", "3. Hypotequer bien1", "3. Hypotequer bien2"])
    hyp_dispo3 = st.number_input("3. Hyp Dispo", value=0, step=5000)
    apport3 = (aprt3*(prix3+travaux3)/100) + (prix3*DrEn3/100)

# st.sidebar.title("ACHAT 3")


# --- ACHAT 4 ---
with st.sidebar.expander("ACHAT 4", expanded=False):  # False = replié par défaut

    preset4 = st.selectbox("Preset Achat 4 (remettre sur -aucun- apres sélection)", presets.keys(), key="preset4")

    if preset4 != "Aucun":
        for k, v in presets[preset4].items():
            st.session_state[f"{k}4"] = v

    capacite_epargne3 = st.number_input("4. PART DE SALAIRE DEDIE AVANT ACHAT 4", value=0, step=50)
    prix4 = st.slider("4. PRIX DU BIEN", min_value=0, max_value=500000, value=st.session_state.get("prix4", 150000), step=5000, key="prix4")
    travaux4 = st.slider("4. PRIX DES TRAVAUX", min_value=0, max_value=500000, value=st.session_state.get("travaux4", 60000), step=1000, key="travaux4")
    estimation4 = st.number_input("4. ESTIMATION DU BIEN", value=prix4+travaux4, step=5000)
    loyer4 = st.number_input("4. LOYER", value=st.session_state.get("loyer4", 1600), step=50, key="loyer4")
    charges4 = st.number_input("4. CHARGES", value=st.session_state.get("charges4", 200), step=50, key="charges4")
    taux4 = st.number_input("4. TAUX", value=st.session_state.get("taux4", 3.5), step=0.1, key="taux4")
    duree4 = st.number_input("4. DUREE DU CREDIT", value=st.session_state.get("duree4", 20), step=5, key="duree4")
    aprt4 = st.number_input("4. APPORT % du prix", value=st.session_state.get("aprt4", 20), step=5, key="aprt4")
    DrEn4 = float(st.radio("4. Droit d'enregistrement 4 :", ["3", "12.5"], index=1, horizontal=True)) + 2
    choix4 = st.selectbox("4. Sélectionne une hypothèque :", ["4.Hyp dispo (saisir valeur)", "4.Aucune hyp dispo", "4.Hypotequer bien1", "4.Hypotequer bien2", "4.Hypotequer bien3"])
    hyp_dispo4 = st.number_input("4. Hyp Dispo: saisir valeur", value=0, step=5000)
    apport4 = (aprt4*(prix4+travaux4)/100) + (prix4*DrEn4/100)

hyp_dict = {
    "4.Hyp dispo (saisir valeur)": lambda: 0.8 * hyp_dispo4,
    "4.Aucune hyp dispo": lambda: 0,
    "4.Hypotequer bien1": lambda: 0.8 * (bien1.amorti[i] + bien1.plusvalue()),
    "4.Hypotequer bien2": lambda: 0.8 * (bien2.amorti[i] + bien2.plusvalue()),
    "4.Hypotequer bien3": lambda: 0.8 * (bien3.amorti[i] + bien3.plusvalue()),
}

#HD4 = hyp_dict[choix4]()  # exécution de la fonction seulement au bon moment

#st.title(HD4)

rp = st.sidebar.radio("Reprise d'encours possible ? (Encours automatique sur achat-1 valorisation non pondéré. Pour le fun)", ["Oui", "Non"], horizontal=True,index=1)
rp_encours = 0 if rp == "Non" else 1


zoom = st.sidebar.slider("REPERE DE PERFORMANCE", 1, 50, 20, step=2)



# apport=(aprt*(prix+travaux)/100)+(prix*DrEn/100)
# if prix > 300000:
#     st.warning("💸 Oh my god. T'as braqué une banque ou quoi?..💳")#https://emojipedia.org/

N=700
class BienImmobilier:
    def __init__(self, valeur, prix, travaux, taux, loyer, charges, duree, apport, bullet, rp_encours,aprt):
        self.aprt=aprt
        self.prix = prix
        self.travaux = travaux
        self.taux = taux / (12*100)  # Taux mensuel
        self.loyer = loyer
        self.charges = charges
        self.duree = duree * 12  # Convertir en mois
        self.bullet = bullet # partie en bullet 0 = pret normal
        self.apport = apport#*prix/100
        self.quotite= (100-self.apport)/100
        self.droit_enregistrement = (prix*DrEn1/100)###########DR1
        self.valeur=valeur
        self.revente = self.valeur* 1#(1+0.01*self.duree ) # Valeur de revente estimée       
        self.cout_acquisition = prix + travaux + self.droit_enregistrement
        self.capital_emprunte = self.prix+self.travaux-(self.prix+self.travaux)*aprt/100 # self.cout_acquisition - self.apport+(prix*DrEn/100) #####aprt1
        self.rp_encours=rp_encours
        self.renta_brut= ((12*loyer)/self.cout_acquisition)*100//1
        self.plusvalue=self.prix + self.travaux - self.valeur 
        self.calculer_mensualites()
        


        #self.printID()

        
    def calculer_mensualites(self):
        aA = (self.capital_emprunte * (1 - self.bullet)) * self.taux / (1 - (1 + self.taux)**-self.duree)
        aB = self.capital_emprunte * self.bullet * self.taux
        self.mensualite = aA + aB
        self.cashflow = self.loyer - self.mensualite - self.charges
        
        self.cap_debut_per=[self.capital_emprunte]
        self.restant_du=[]
        self.interet=[]
        self.amorti=[]
        self.cashflow_list=[]
        

        for i in range(self.duree):
            self.interet.append(self.cap_debut_per[i]*self.taux)
            self.amorti.append(self.mensualite-self.interet[i])
            self.restant_du.append(self.cap_debut_per[i]-self.amorti[i])
            self.cap_debut_per.append(self.restant_du[i])
            self.cashflow_list.append(self.cashflow)
            
        while len(self.cap_debut_per) < N+1: #Longueur de la liste d analise. Je me des zero  a la fin des listes pour qu'elles soient de longueur N
            
            if self.bullet==0:
                self.cashflow_list.append(self.loyer-self.charges)
            else:
                self.cashflow_list.append(0)
            self.cap_debut_per.append(0)
            self.restant_du.append(0)
            self.interet.append(0)
            self.amorti.append(0)
        if self.bullet !=0 :
            self.cashflow_list[self.duree]=self.revente-self.capital_emprunte*self.bullet#(1-self.bullet)*self.capital_emprunte
    def printID(self):
        print ("capital emprunter =", self.capital_emprunte, "\nmensualité =", self.mensualite//1,"\nloyé =", self.loyer//1, "\n cashflow =", self.cashflow//1,"\n ")
    def get_info(self):
        info = f"""Capital emprunté = {int(self.capital_emprunte)}€
\nApport + Droit d'enregistrement = {int(self.apport)}€
\nMensualité = {int(self.mensualite)}€
\nLoyer = {int(self.loyer)}€
\nCharges = {int(self.charges)}€
\nRevenu locatif = {int(self.loyer-self.charges)}€
\nCashflow = {int(self.cashflow)}€
\nNouvelle capacite d'epargne = {int(capacite_epargne0+self.cashflow)}€
"""
        return info

    def move(self):
        self.cap_debut_per.insert(0,0)#Ajoute sero en position zero
        self.cap_debut_per.pop() #supprime le dernier ellement de la liste (derier par défaut si index non spécifié)
        self.restant_du.insert(0,0)
        self.restant_du.pop()
        self.interet.insert(0,0)
        self.interet.pop()
        self.amorti.insert(0,0) 
        self.amorti.pop()
        self.cashflow_list.insert(0,0) 
        self.cashflow_list.pop()
    
#bien1 = BienImmobilier(prix=100000, valeur=100000, bullet=0, travaux=0, taux=0.035, loyer=900, charges=100, duree=25, apport=25000, rp_encours=0 )
bien1 = BienImmobilier(prix=prix1, valeur=estimation1, bullet=0, travaux=travaux1, taux=taux1, loyer=loyer1, charges=charges1, duree=duree1, apport=apport1, rp_encours=rp_encours, aprt=aprt1)
bien2 = BienImmobilier(prix=prix2, valeur=estimation2, bullet=0, travaux=travaux2, taux=taux2, loyer=loyer2, charges=charges2, duree=duree2, apport=apport2, rp_encours=rp_encours, aprt=aprt2)
bien3 = BienImmobilier(prix=prix3, valeur=estimation3, bullet=0, travaux=travaux3, taux=taux3, loyer=loyer3, charges=charges3, duree=duree3, apport=apport3, rp_encours=rp_encours, aprt=aprt3)
bien4 = BienImmobilier(prix=prix4, valeur=estimation4, bullet=0, travaux=travaux4, taux=taux4, loyer=loyer4, charges=charges4, duree=duree4, apport=apport4, rp_encours=rp_encours, aprt=aprt4)
#print(bien1.restant_du)
#print(bien1.cap_debut_per)
#print(bien1.mensualite)

tx_endt1=(bien1.mensualite/(bien1.loyer+salaire))*100//1
tx_endt2=((bien1.mensualite+bien2.mensualite)/(bien1.loyer+bien2.loyer+salaire))*100//1
tx_endt3=((bien1.mensualite+bien2.mensualite+bien3.mensualite)/(bien1.loyer+bien2.loyer+bien3.loyer+salaire))*100//1
tx_endt4=((bien1.mensualite+bien2.mensualite+bien3.mensualite+bien4.mensualite)/(bien1.loyer+bien2.loyer+bien3.loyer+bien4.loyer+salaire))*100//1

class joueur :
        def __init__(self, epargne, capacite_epargne0,capacite_epargne1, capacite_epargne2, capacite_epargne3, duree_analyse, hypotheque_dispo):
            self.epargne=epargne
            self.economie0=capacite_epargne0
            self.economie1=capacite_epargne1
            self.economie2=capacite_epargne2
            self.economie3=capacite_epargne3
            self.N_analyse=duree_analyse*12
            self.hypotheque_dispo=hypotheque_dispo
J=joueur(epargne= epargne, capacite_epargne0=capacite_epargne0, capacite_epargne1=capacite_epargne1, capacite_epargne2=capacite_epargne2, capacite_epargne3=capacite_epargne3, duree_analyse= 50, hypotheque_dispo=hyp_dispo1)##### hip dispo 1


#PHASE 0 : condition fin economie = apport.
#PHASE 1 : CASHFLOW + Reprise encour = apport
#PHASE 2 : CASHFLOW + Reprise encour = apport
#PHASE 3 : CASHFLOW + Reprise encour = apport
#st.title(bien1.mensualite())



CASHFLOW = [epargne]
DETTE = []
GAIN = [0]
DEPMENS=[salaire-capacite_epargne0]
TAUX_ENDT=[0]

# Périodes analysées en mois
N = list(range(0, J.N_analyse, 1))

phase = 0
count0 = 0
count1 = 0
count2 = 0
count3 = 0
counttot=0



for i in N:
    if phase == 0:
        #print("phase=O")
        count0 += 1
        DETTE.append(0)
        DEPMENS.append(salaire-capacite_epargne0)
        TAUX_ENDT.append(TAUX_ENDT[-1])
        #GAIN.append(0)
        if CASHFLOW[-1] + J.hypotheque_dispo < bien1.apport:
            CASHFLOW.append(CASHFLOW[-1] + J.economie0)#attention dans ppt economie != cashflow
            GAIN.append(CASHFLOW[-1])
            bien1.move()
            bien2.move()
            bien3.move()
            bien4.move()
        else:
            CASHFLOW[-1] = CASHFLOW[-1]-bien1.apport#retombe a zero, mais attention si hypothèque ou reprise d'encours dispo la remise a zero du compte ets pas forcement correcte
            
            phase = 1
    
    elif phase == 1:
        #print("phase=1")
        count1 += 1
        #print(count1)
        dette_phase1 = -bien1.restant_du[i] #RestantDu1[i - count0 ] 
        DETTE.append(dette_phase1)
        gain_phase1 =  dette_phase1 + bien1.revente + CASHFLOW[-1]#GAIN[-1]+
        GAIN.append(gain_phase1)
        DEPMENS.append(salaire-capacite_epargne1)
        TAUX_ENDT.append(bien1.mensualite/(bien1.loyer+salaire))
        
        bien2.move()
        bien3.move()
        bien4.move()
        #print("B1 RD=",(bien1.restant_du[count0+count1]),bien1.revente)
        if CASHFLOW[-1]  < bien2.apport or nbbien==1 :
            CASHFLOW.append(CASHFLOW[-1] + J.economie1 + bien1.cashflow_list[i])
        elif bien1.rp_encours == 1 and CASHFLOW[-1] +(bien1.revente - bien1.restant_du[count0+count1]) < bien2.apport:
            #print("Rp dispo=",(bien1.revente - bien1.restant_du[count1]))
            CASHFLOW.append(CASHFLOW[-1] + J.economie1 + bien1.cashflow_list[i])

        else:
            if bien1.rp_encours == 1:
                CASHFLOW[-1] = CASHFLOW[-1]-(bien2.apport-(bien1.revente - bien1.restant_du[count0+count1]))
            if bien1.rp_encours == 0:
                CASHFLOW[-1]=0
            phase = min(2, nbbien)#phase = 2
    
    elif phase == 2:
        #print("phase=2")
        count2 += 1
        dette_phase2 = -bien1.restant_du[i] - bien2.restant_du[i] 
        DETTE.append(dette_phase2)
        gain_phase2 = dette_phase2 + bien1.revente + bien2.revente + CASHFLOW[i-2]
        GAIN.append(gain_phase2)
        bien3.move()
        bien4.move()
        DEPMENS.append(salaire-capacite_epargne2)
        TAUX_ENDT.append((bien1.mensualite+bien2.mensualite)/(bien1.loyer+bien2.loyer+salaire))
        
        # if CASHFLOW[-1] < bien3.apport:
        #     CASHFLOW.append(CASHFLOW[-1] + J.economie + bien1.cashflow_list[i] + bien2.cashflow_list[i])
        if bien2.rp_encours == 0 and CASHFLOW[-1]  < bien3.apport or nbbien ==2:
            CASHFLOW.append(CASHFLOW[-1] + J.economie2 + bien1.cashflow_list[i]+ bien2.cashflow_list[i])
        elif bien2.rp_encours == 1 and CASHFLOW[-1] +(bien2.revente - bien2.restant_du[count0+count1+count2]) < bien3.apport:
            CASHFLOW.append(CASHFLOW[-1] + J.economie2 +  bien1.cashflow_list[i]+ bien2.cashflow_list[i])        
        else:
            if bien2.rp_encours == 1:
                CASHFLOW[-1] = CASHFLOW[-1]-(bien3.apport-(bien2.revente - bien2.restant_du[count0+count1+count2])) 
            if bien2.rp_encours == 0:
                CASHFLOW[-1]=0
            phase = min(3, nbbien)#phase = 3

    # if counttot>count1+N1 :
    #     Cashflow1=Loyer1
        
    elif phase == 3:
        HD4 = hyp_dict[choix4]() ##########################################################################################
        #print("phase=3")
        # if RestantDu1[i] <100 and bullet1 !=0:
                  
            # dette_phase3 = -bien1.restant_du[i] - bien2.restant_du[i] -bien3.restant_du[i] 
            # DETTE.append(dette_phase3)
            # gain_phase3 = dette_phase3 + bien1.revente + bien2.revente + bien3.revente + CASHFLOW[i-3] 
            # GAIN.append(gain_phase3)
        
            # CASHFLOW.append(CASHFLOW[-1] + J.economie + bien1.cashflow_list[i] + bien2.cashflow_list[i] + bien3.cashflow_list[i])
######################
        count3 += 1
        dette_phase3 = -bien1.restant_du[i] - bien2.restant_du[i] - bien3.restant_du[i] 
        DETTE.append(dette_phase3)
        gain_phase3 = dette_phase3 + bien1.revente + bien2.revente + bien3.revente + CASHFLOW[i-3]
        GAIN.append(gain_phase3)
        bien4.move()
        DEPMENS.append(salaire-capacite_epargne3)
        TAUX_ENDT.append((bien1.mensualite+bien2.mensualite+bien3.mensualite)/(bien1.loyer+bien2.loyer+bien3.loyer+salaire))
        
        # if CASHFLOW[-1] < bien3.apport:
        #     CASHFLOW.append(CASHFLOW[-1] + J.economie + bien1.cashflow_list[i] + bien2.cashflow_list[i])
        if bien3.rp_encours == 0 and CASHFLOW[-1]  < bien4.apport or nbbien ==3:
            CASHFLOW.append(CASHFLOW[-1] + J.economie3 + bien1.cashflow_list[i]+ bien2.cashflow_list[i]+ bien3.cashflow_list[i])
        #elif bien3.rp_encours == 1 and CASHFLOW[-1] +(bien3.revente - bien3.restant_du[count0+count1+count2+count3]) < bien4.apport:
        elif bien3.rp_encours == 1 and 1.15*bien4.prix + bien4.travaux - bien4.quotite * (HD4+0.8*(bien4.prix + bien4.travaux))< CASHFLOW[-1]: ######################################
            CASHFLOW.append(CASHFLOW[-1] + J.economie3 +  bien1.cashflow_list[i]+ bien2.cashflow_list[i]+ bien3.cashflow_list[i])        
        else:
            if bien3.rp_encours == 1:
                CASHFLOW[-1] = CASHFLOW[-1]-(bien4.apport-(bien3.revente - bien3.restant_du[count0+count1+count2+count3])) 
            if bien3.rp_encours == 0:
                CASHFLOW[-1]=0
            phase = min(4, nbbien)#phase = 3
    elif phase == 4:
            
        #if RestantDu1[i] <100 and bullet1 !=0:
                  
            dette_phase4 = -bien1.restant_du[i] - bien2.restant_du[i] -bien3.restant_du[i] -bien4.restant_du[i] # probleme avec bien4.restant_du[i] le restant du devrait etre plus grand 90k pas 70k
            DETTE.append(dette_phase4)
            #print("RD4 =",bien4.restant_du[i])
            gain_phase4 = dette_phase4 + bien1.revente + bien2.revente + bien3.revente + bien4.revente + CASHFLOW[i-4] 
            GAIN.append(gain_phase4)
            DEPMENS.append(salaire-capacite_epargne3)
            TAUX_ENDT.append((bien1.mensualite+bien2.mensualite+bien3.mensualite+bien4.mensualite)/(bien1.loyer+bien2.loyer+bien3.loyer+bien4.loyer+salaire))
        
            CASHFLOW.append(CASHFLOW[-1] + J.economie3 + bien1.cashflow_list[i] + bien2.cashflow_list[i] + bien3.cashflow_list[i]+ bien4.cashflow_list[i])

####################
eco_fictive=[0]
for i in range(len(N)):
    eco_fictive.append(eco_fictive[i]+J.economie1)

def equalize_lists(*lists):
    min_length = min(len(lst) for lst in lists)
    return [lst[:min_length] for lst in lists]

N, CASHFLOW, DETTE, GAIN, eco_fictive, DEPMENS, TAUX_ENDT = equalize_lists(N, CASHFLOW, DETTE, GAIN, eco_fictive, DEPMENS, TAUX_ENDT)

# ecarts = [abs(DETTE[i+1] - DETTE[i]) for i in range(len(DETTE) - 1)]

# # Trouver le plus grand de ces écarts
# Mensualite_max = max(ecarts)

# print("Mensualité max =", Mensualite_max)

# print("len Dette =", len(DETTE))
# print("len CASHFLOW =", len(CASHFLOW))
# print("len N =", len(N))

Na = [n / 12 for n in N]

# Trouver l'indice correspondant à 10 ans
index_10_ans = Na.index(zoom)
#index_20_ans = Na.index(30)

# Valeur du GAIN à 10 ans
gain_10_ans = round( GAIN[index_10_ans],-3)
#gain_20_ans = round( GAIN[index_20_ans],-3)

FinA1= (count0+(bien1.duree))/12
FinA2= (count0+count1+(bien2.duree))/12
FinA3= (count0+count1+count2+(bien3.duree))/12

# Création de la figure et des axes
fig, ax = plt.subplots()
#fig, ax = plt.subplots(figsize=(10, 10))

# Courbes principales
ax.plot(Na, CASHFLOW, linestyle='-', label="Cashflow")
ax.plot(Na, DETTE, label="Dette")
ax.plot(Na, GAIN, label="Cash + patrimoine acquis")
ax.plot(Na, eco_fictive, linestyle='-', label="eco fictive")

# Points rouges (gain à 10 et 20 ans)
ax.scatter(zoom, gain_10_ans, color='red')
ax.text(zoom, gain_10_ans, f' {gain_10_ans:.0f}', color='red', fontsize=12, verticalalignment='bottom')

# ax.scatter(30, gain_20_ans, color='red')
# ax.text(30, gain_20_ans, f' {gain_20_ans:.0f}', color='red', fontsize=12, verticalalignment='bottom')

# Points verts (fin crédits)
ax.scatter(FinA1, 0, color='green')
# ax.text(FinA1, 0, ' Fin crédit 1', color='green', fontsize=12, verticalalignment='bottom')

ax.scatter(FinA2, 0, color='green')
# ax.text(FinA2, 0, ' Fin crédit 2', color='green', fontsize=12, verticalalignment='bottom')

ax.scatter(FinA3, 0, color='green')
# ax.text(FinA3, 0, ' Fin crédit 3', color='green', fontsize=12, verticalalignment='bottom')

# Mise en forme
ax.set_title('YA')
ax.set_xlabel('Ans')
ax.set_ylabel("Euros")
ax.legend(loc='best')
ax.grid(True)

ax.set_xlim([0, 50])
ax.set_ylim([-300000, 800000])
# Affichage Streamlit

##############################


############# AFFICHAGE CAP EMPRUNT

RAV=st.number_input("RESTE A VIVRE LIMITE (achat1)", value=1500, step=100)
diff=(salaire-bien1.mensualite)
# 🟢 ou 🔴 mise en forme conditionnelle :
if  RAV<=salaire-bien1.mensualite:
    couleur_fond = "#e6ffe6"  # vert très clair
    couleur_texte = "green"
    message = f"✅ Reste a vivre OK : {diff:,.0f} €/mois".replace(",", " ")
    #message = f"✅ Reste a vivre OK : {diff:,.0f} €/mois"
else:
    couleur_fond = "#ffe6e6"  # rouge très clair
    couleur_texte = "red"
    message = f"❌ Reste a vivre inssufisant : {diff:,.0f} €/mois"

st.markdown(
    f"""
    <div style="
        padding: 0.8em;
        background-color: {couleur_fond};
        color: {couleur_texte};
        border: 2px solid {couleur_texte};
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1em;
    ">
        {message}
    </div>
    """,
    unsafe_allow_html=True
)
######################


####################
taux_endettement = [tx_endt1, tx_endt2, tx_endt3, tx_endt4]
# Ne garder que les taux des biens sélectionnés
taux_endettement_sel = taux_endettement[:nbbien]
taux_limite=st.number_input("TAUX D'ENDETTEMENTLIMITE", value=40, step=5)
# Boucle dynamique selon le nombre de biens
for i, taux in enumerate(taux_endettement_sel, start=1):
    if taux < taux_limite:
        couleur_fond = "#e6ffe6"  # vert très clair
        couleur_texte = "green"
        message1 = f"✅ Bien {i} : Taux d'endettement = {taux/100:.0%} < {taux_limite}%"
    else:
        couleur_fond = "#ffe6e6"  # rouge très clair
        couleur_texte = "red"
        message1 = f"⚠️ Bien {i} : Taux d'endettement = {taux/100:.0%} ≥ {taux_limite}%"

# taux_limite=st.number_input("TAUX D'ENDETTEMENTLIMITE", value=40, step=5)
# taux_endettement = [tx_endt1, tx_endt2, tx_endt3, tx_endt4 ]
# for i, taux in enumerate(taux_endettement, start=1):
#     if taux < taux_limite:
#         couleur_fond = "#e6ffe6"  # vert très clair
#         couleur_texte = "green"
#         message1 = f"✅ Bien {i} : Taux d'endettement = {taux/100:.0%} < 50%"
#     else:
#         couleur_fond = "#ffe6e6"  # rouge très clair
#         couleur_texte = "red"
#         message1 = f"⚠️ Bien {i} : Taux d'endettement = {taux/100:.0%} ≥ 50%"

# 💬 Affichage stylé :
st.markdown(
    f"""
    <div style="
        padding: 0.8em;
        background-color: {couleur_fond};
        color: {couleur_texte};
        border: 2px solid {couleur_texte};
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1em;
    ">
        {message1}
    </div>
    """,
    unsafe_allow_html=True
)
###############
st.header("Investissement")
st.pyplot(fig)

###################

# Variables (à remplacer par tes calculs)
mensualite= [bien1.mensualite//1, bien2.mensualite//1, bien3.mensualite//1, bien4.mensualite//1]
renta = [bien1.renta_brut, bien2.renta_brut, bien3.renta_brut, bien4.renta_brut]
taux_endettement = [tx_endt1, tx_endt2, tx_endt3, tx_endt4 ]
cashflow = [bien1.cashflow//1, bien2.cashflow//1, bien3.cashflow//1, bien4.cashflow//1]

# Construire un tableau avec 4 colonnes fixes
data = {}
for i in range(4):
    if i < nbbien:
        data[f"Bien {i+1}"] = [mensualite[i], renta[i], taux_endettement[i], cashflow[i]]
    else:
        data[f"Bien {i+1}"] = ["-","-","-","-"]

df = pd.DataFrame(
    data,
    index=["Mensualité €","Renta brute %", "Taux d'endettement %", "Cashflow €"]
)

st.dataframe(df, use_container_width=True)


###############
st.header("Confort de vie")
st.write("Work in progresse. Ici bientôt, votre confort de vie. Car après tout, c'est ça qu'on cherche !")
# Tes listes
Na=Na
Dep_Mens =  DEPMENS
#achat_index = 100  # index du point d'achat
fig, ax = plt.subplots(figsize=(10, 3))  # largeur = 10, hauteur = 5
# Créer le graphique

ax.plot(Na, Dep_Mens, marker='o', color="#49DF64",label="Dépense mensuelle")
ax.axhline(y=salaire, color="#FF6B6B", linestyle="--", linewidth=2, label=f"Salaire = {salaire} €")
#ax.text(Na[achat_index], Dep_Mens[achat_index]+50, "🏠", fontsize=14, ha='center') 


ax.set_title("Ce que tu décide de dépenser chaque mois")
ax.set_xlabel("Année")
ax.set_ylabel("Dépense Mensuelle (€)")
ax.legend(loc='best')
ax.set_xlim([0, 50])
ax.set_ylim([1000, 4000])
ax.grid(True)

# Afficher dans Streamlit
st.pyplot(fig)

####################





####################

# txt = bien1.get_info()
# st.header("INFO")
# st.write(txt)#(f"Reste a vivre: **{(RAV):,.0f} €/mois**")

################

import random


# --- Banque de messages/émotions par thème
themes = {
    "prix_bas": [
        ("Esperons que ça passe ! ", "https://image.noelshack.com/fichiers/2025/17/4/1745527651-espoire.jpg"),
        ("On en sait jamais trop ? ", "https://image.noelshack.com/fichiers/2025/17/4/1745525443-sourir.jpg"),
        ("Oh yeah? C’est cadeau.", "https://image.noelshack.com/fichiers/2025/17/4/1745527749-formidable.jpg")
    ],
    "prix_haut": [
        ("NAAAA, c’est trop cher !", "https://image.noelshack.com/fichiers/2025/17/4/1745525501-aieaie.jpg"),
        ("Tu veux acheter un château ? ", "https://image.noelshack.com/fichiers/2025/17/4/1745527487-naze.jpg"),
        ("Y a pas un problème là…", "https://image.noelshack.com/fichiers/2025/17/4/1745527549-revolte.jpg")
    ],
    "duree_courte": [
        ("Woh, 15 ans ?! Tu vas souffrir sur les mensualités ", "https://image.noelshack.com/fichiers/2025/17/4/1745525501-aieaie.jpg"),
        ("Tu veux être libre vite ou t’as oublié de simuler ?", "https://image.noelshack.com/fichiers/2025/17/4/1745527357-bofbof.jpg"),
    ],
    "endettement_eleve": [
        ("Attention, t’es au taquet niveau endettement !", "https://image.noelshack.com/fichiers/2025/17/4/1745527549-revolte.jpg"),
        ("Tu sais qu'il y a deutre type de crédit?", "https://image.noelshack.com/fichiers/2025/17/4/1745525501-aieaie.jpg"),
    ],
    "reste_a_vivre_faible": [
        ("Tu vas manger des pâtes… mais avec un bien locatif ", "https://image.noelshack.com/fichiers/2025/17/4/1745527357-bofbof.jpg"),
        ("Reste à vivre serré, t’es sûr de ton coup ?", "https://image.noelshack.com/fichiers/2025/17/4/1745527487-naze.jpg"),
    ]
}

# --- Logique de sélection du thème dominant
messages_possibles = []

if prix1 < 90000:
    messages_possibles.extend(themes["prix_bas"])
elif prix1 > 250000:
    messages_possibles.extend(themes["prix_haut"])

if duree1 < 15:
    messages_possibles.extend(themes["duree_courte"])

# if endettement > 0.35:
#     messages_possibles.extend(themes["endettement_eleve"])

# if reste_a_vivre < 1200:
#     messages_possibles.extend(themes["reste_a_vivre_faible"])

# Fallback si aucun critère déclenché
if not messages_possibles:
    messages_possibles.extend(themes["prix_bas"])  # ou créer un thème "neutre"

# Choisir un message aléatoirement dans la sélection
message, image_url = random.choice(messages_possibles)

# --- Affichage HTML avec style Streamlit
st.markdown(f"""
    <style>
    .fixed-avatar {{
        position: fixed;
        top: 220px; 
        right: 20px; 
        width: 100px;
        border-radius: 50%;
        z-index: 1000;
    }}
    .fixed-text {{
        position: fixed;
        top: 130px; 
        right: 20px; 
        width: 250px;
        background-color: white;
        padding: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        z-index: 1000;
        font-family: sans-serif;
    }}
    </style>

    <img src="{image_url}" class="fixed-avatar">
    <div class="fixed-text">
        <p>{message}</p>
    </div>
""", unsafe_allow_html=True)


################
# if prix > 200000:
#     message = "NAAAA, c'est trop cher!"
#     image_url= "https://image.noelshack.com/fichiers/2025/17/4/1745525501-aieaie.jpg"
# if prix < 200000:
#     message = "Ca te plait l'investissement?"
#     image_url= "https://image.noelshack.com/fichiers/2025/17/4/1745525443-sourir.jpg "


# # Injecter dynamiquement l'image et le message dans le HTML/CSS
# st.markdown(f"""
#     <style>
#     .fixed-avatar {{
#         position: fixed;
#         top: 220px; 
#         right: 20px; 
#         width: 100px;
#         border-radius: 50%;
#         z-index: 1000;
#     }}

#     .fixed-text {{
#         position: fixed;
#         top: 130px; 
#         right: 20px; 
#         width: 250px;
#         background-color: white;
#         padding: 10px;
#         box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
#         z-index: 1000;
#         font-family: sans-serif;
#     }}
#     </style>

#     <img src="{image_url}" class="fixed-avatar">
#     <div class="fixed-text">
#         <p>{message}</p>
#     </div>
# """, unsafe_allow_html=True)
##############################


#with open(r"C:\Users\hugod\OneDrive\Bureau\Bureau\IMO\mon_fichier.pdf","rb") as f:
#    pdf_bytes = f.read()
with open("assets/mon_fichier.pdf", "rb") as f:
    pdf_bytes = f.read()

st.sidebar.download_button(
    label="📄 Télécharger explications du code",
    data=pdf_bytes,
    file_name="Code Immo.pdf",
    mime="application/pdf"
)



# https://image.noelshack.com/fichiers/2025/17/4/1745525443-sourir.jpg 
# https://image.noelshack.com/fichiers/2025/17/4/1745525501-aieaie.jpg
#https://image.noelshack.com/fichiers/2025/17/4/1745527357-bofbof.jpg
# https://image.noelshack.com/fichiers/2025/17/4/1745527487-naze.jpg
#https://image.noelshack.com/fichiers/2025/17/4/1745527549-revolte.jpg
#https://image.noelshack.com/fichiers/2025/17/4/1745527749-formidable.jpg
# https://image.noelshack.com/fichiers/2025/17/4/1745527651-espoire.jpg 
#print(eco_fictive)
#print(GAIN)
#print(bien1.restant_du)
# print(bien1.cashflow_list)
# print(bien3.cashflow_list)



