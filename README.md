# IIIFDexir Project  

The IIIFDexir project is a dynamic catalog based on IIIF. It emphasizes several technical features:  

## Key Features  

- Machine Readability: The catalog is designed to be machine-readable and consumable.
- Linked Data. IIIFDexir is fully compatible with Linked Data Paradigm and LOUD/FAIR concepts. 
- IIIF Compatibility: IIIFDexir is fully compatible with IIIF standards.  
- Hierarchical Arrangement: Resources in the catalog are all IIIF Manifests accessible online and are arranged hierarchically as nested Multipart IIIF Collection.  
- Flexible Data Structures: The data structures of the resources in the collection are JSON-LD compatible and highly flexible that can be enriched with external data sources, including XML, JSON, and RDF files.  
- Controlled Vocabularies: IIIFDexir is associated with standard controlled vocabularies and knowledge baeses like AAT, TGN, LCSH, TGM and Wikidata. In some circumestances I extend The AAT and TGM with new terms and concepts to demonstrate how easy is extending the contolled vocabularies.
- FHKB (Family History Knowledge Base). A Full version of FHKB is embeded into the project for the Agential data.  
- On The Fly Manifests. There are many use cases that we want to use a customize curated manifests from selected cavases that physically belong to other manifests. There is a python code to achive this goal which provided with some samples. These manifests are hosted locally.
- Human Usability: While the primary focus is on machine consumption, the catalog is also usable by humans via standard IIIF viewers like Mirador and OpenSeaDragon.  
- Public Accessibility: The catalog remains publicly accessible.  
![IIIFDexir](/IIIFCollection/images/IIIFDexir.JPG)

## Subset of AAT concepts used in IIIFDexir
AAT has a hierarchical structure with 7 Facets as root many sub Branches related to Art and Architecture which has very critical role in IIIFDexir.
Below is a subset of AAT collection with limited scope suitable for use in IIIFDexir:

![AAT Subset](https://mermaid.ink/img/pako:eNqNfW2P5LiR5l9J1H5wN9Bt6IWvvQMD9swucAd4MXfj2wVuZ2EolaosTStTOZKyq2sM_6D9D_fNf-wYEVlZIhUhtb1YuCuefEjxJRgkI4J_e6j7Q_Pw6eGx65_rp2qYdn_508_n3a7uqnH8oXncnfvhVHW7x7brPv3TYwH__TBOQ_-5-fRPzrnb__743B6mp0_55es_R78-XttD85dmOL0SPD4WVX0n2Dv3mGUbHM3XqTkfmsNPdX9pbjz1Y1M8lneecm91ZTd49v309FoNVYf_3H9eleW-3PM_r6qpzLKssIVx__nzQ3U4tec2IKup_dLshubSD9P488_nd3Pg-58f_utedkRxa8-Y2avAXPen0_Xc_nptEjqvJDqveDob6C5ddR53724VfJ9QWpHScpRlboBy6OumObTno0QccAJxkLDERRmIp6Z-Ord1GGZcewaMRFqUbAMYaID_TVQfdv-zvw7nqgu_Ox92P_T19dScF10mNojhGsSYDBrkT33_efd9NVVdf4wIQc4TgmRBmDtvMhgDf67O17Ee2su0-9e-a_s3ToJwnCRZcubaldC4XVN9aUKHHavpqRmaw-5UTVMzzDqOoCw3SpbcXueFDtz7MMg-76iEGR-KWT6ULPmMUzYPfEkdd2FOXPpz3F0EZtlRsmAvsrwwRWBvz48gmtr-vIP_xdITmqMnyZJehUaCzvvujW63f9mNl6ZuH9s6lHKegg77w6wM_AlbBkre1OasmFyXzodi_u25GS_VpRloQP-5Ola_ted5-xOUpUcJO6A1Ko1maPsDzMRkOGsrDWfNzw8FDT4GOph47y7XfRdYoeVjjQFAiVkVzKDOvYdGmBPu3h1eJ3U0qAHKD2qQcLXOShiEr2y7Y3MeYmUMCKG6QbIcGkWmiwyGxr2GMDLCgDi0VPX-cRe06uFawz_nIwR_yXYhSrgRkpfWa7UoDUb6jJlQbLugRGTWS-brOa03IUV2vWSn1nPW4hI4hAYPc-jQnOvmlfWOWNLeRVxvOutoVs5Jod5tmI-wIqRNQ78R-jdIuKZBiUc1CxorDMa4vPcJvRfp2RHpHMyjuh3qa1cNu1shMaeTZlCQ8JwwSELlXupuOdWdUyKd4unQNqguoUFlUiOSGp4U-g6VNP_NYjc5x_L5bNZHYdZVhy_t2xB7xUikPuNJi5gUBtZ5SkjF3vF873gTkw4NWIbBAkZtl5CLzerZZvVoZXR9sFy5ZvWZ1Pc-Y_veo124v46wAI08p2QSgoTnhK4fq66RCJ1IuOz70iqaQ3E33XXuGzUhOWqSMNTaarCwwnRvj2eyKxY1JhRPC5Ilrc-8Am14bpvr8y9VNYz7oW2-NPO6IoYlRcmCVBXeKY91fWyGIUzVRUUJwnGSZMlZ6sImgxWWtr6ba-9XHEuMEtZ-cBorG5TpQVjgCSUZD05ztMrAAl8_DWEH15zDRiZsCvvP8fgKGIE0SLjtRq6gEU7NEPbPYWEfmzDAQm9Nfei1eJsRkMI2I0jY7ZFGM-qpvYy_25HRF2-NdCFtjTSnXaw1uIy_NmxYDIP5ESpbhR6LVkJACtRBwq-E1tqCVvGw86LpcCsoZrZSpYOErTQaB8dQz-GMhhnPakVWdk9rHbB-t6QVTBv6iVSGs1Kb4MrzXfO1qa-3I4PttpdWIpCI5cDQ_uUarPcWVuK0vKSAXCyAHePWl3gAEDRdMGsmKIEZjgEl0pY8rRYbR-gCLw5LLw1Lh6tefR2n_jSy7eGkhQ8kXMUd7v_f6h0Y08Zw0hEASHhOWPja06k9rsyegBJp2dMll_tYR5-q4ddrE5PmXiLNPUtazO2pS5XaPQCQGIuMZ8xvjGGQ7Q7Nrq7qpyYlzUXSnCcFhXRqu3aqhhe-PYtC5GS1kSvh08Nyfw3LaPvbSk-VYhOUfBPg9vNSDYewNUyoxA8v-Q8vC6SaFkddQSJS8d-LW_mhOYYdyG2_vZiv8SmgU2IRii9CZ3PdxTamFhtT842pYYZ-l5K-7ojDjBU0TPihWJKRNAyenhyauh2phdJikwaSjlNAwn8MzOHxur_0Yb1IW0acu5qfuyZDstMpVDWxUIJMIjN8MxvQrc9Dmw4zI2pUw2tUsky4_pKWSSeaKE40UZwxuKH-0nbBWL0OvDERUCIzr7sdrI_10J5aOFhYYXbSEhkkPLNGvXhsx64SF3TnxKZgLeHwZ7R-GN5vmCGiGeREM4g29Pu2g-NAptRkgjhxkXP8Iud80kpVnY5IJ84T9kjU0mZZaiJpUIp7aJAIjeMzjXbz-RjWPtAgghIMOJGb7WWfa1pRurYCExcWQcZuCzCJN-d5CyXbzmLLFGLLFGLLFA5b5nqeXnYbO4CAFfnZQeNxvYVLt7qF06stfnER9vwi7EuLtw7BRnqjlrq2tCI5uyR4OmGfwhK_WXFxPfb8euyVJhOHhuImvTh6FD96FB7uNcFk_hZ2sVcV36u4Fj_146UVG1tcfz2__npcf09VELUipxc5efViShx9Y3M98YxGWiqChGfEQ_Sn61A_CYzidxv-u43HI_SIcnuBCD8Ty_HSTLdgleyry9SO4HBQN8ME12dhfCcfYSUTJUjYj6BTCfqG_bULe4z2nHKKM4Q_kvB48PVW2wEWiWmhV60RaQ1Pi6vk9TbKeE5xPlh-Pjho2NBRONsEUie2qePb9HbjuRgYovJ3ovJ3ovJ3b-P5OeyKmvP4u7Cu42qQ1l8c2I4f2Hh0f2j7uhkrfvvmvTgmPD8m0I0jLLZ9_SRqCdGZw_POHN7T7crQjk_iuaL34jhj7wFchqbNWD_1PVtPAPCMIOEZPZ6xDEMLV1UJmRfJPEuW4z1se-n6U5VULM8lrjznuaCnH6tQq4kzfgAgMhY8IzTecagOzfL4GKQiHd9yOR11g7fKrq4WPSHZZiBh-QoYMeNL11X7NqYqjERV8MMEra_pqUm2iSAQmRzP5LFHxzGodTpGSAjFIVLwQ6S8-SuMaKJw_SpZVCBhKRUqyurUdvxAUZlEqDKesCCvqce7Vc_SiuOPs86Us3j21nx9avetcPiEIJYVJTxr8ca6IyeklLIQKZmKwmk-WjgVrje7xTBCAMuIEsb5oyxwM9yQ1bv4bALwLh8gWTKWhk63-sdHOnU4LN3DCMS7NBjuQCv82WcwOv_U7juumigXCINkSahyg-fv94vWJSdCWE6ULDl1kRXF_eIebhgf53woZvlQwvIphXXELT7RLjf3hJOIFePHZpTFXj_3Yfsq9RGCeJ8wkDCs2mB1w9Ac2kkw6wnF04JkSWsLq-ObgSUpYlhSlDD-a9qjahoasILoDL8JtZ47rQGEd1oDyZJTm1zj1npmZpO3AdiHw8vuXXTrOOtB-ilbFkqWZZnC4JJZhw_YdYF-7quGQpYNJTwbjIc_N4cWeq86N8GCu4QfJq6jhBSpNUdNdzDNeei7jvyc5HZAtEDP3cUUpizw3ATqWR2D8QCnYXNCkPOEIGEJ0UQem2p5n09SiY4xi8u8yHAHWYUhMU7gKj3X1yRmfQ5QwvOhz3Sw30NX1dPvRpbUiaSOJyVHhqlqO94kJpDI6llW3H-GCdY89WFPno5TQkiUzMYT_5zfXRWXeoAAImPOM9IFO54u99HoIalIV_B0sKp8aXDC8xUsRcaSZ8TrgKrrdsH8bBYVVCKd4ukMOWSGHgbNz9uPBBSZDc9sSfufFjYZSUU6ZqD7PM_dmws_mmSLbTaheJ8dkCz9a3Jr0WenqsNW4xTGkPD9BGQdbFDCeAOVBerQOhiQv4VtdVBxwoELQXmvIJAw3KrI7ey-_dCEXw2LOiOM5wUJw2s17mzut7mhNSBi5RhXF1A8LUg4WoP-Yb9cD8dTdItNIoHLMA5hqszoJjOY_PvQjHMXqEy4wCQJQ5U7XPNDf4Oj4nJ2EoKnBAlDqXJNN3_DAAE1A2dJEYqnBQlHq3B1n6qvqU4imUCmmMVdlcGgBp303dScwIkodHPVXZ6CKpkwPgS08ifmyPgP80KBgy8UJNxhk9Laleh2-HKujv3xyjU4YlhelCw_Bv6M58b9-KvI6EVG9tRY0c3LNx_FKvHSRYmXLvrmLHvkjW1CCKyadZW1JZ4XTkMFG61d6MvPTRrlIx4QlqzfsdUlHsG2h92-PyfHbEEm1a9kD141nt1B7Q7Vl3bxtUr8Wr5q_tWMqrvm5nI684pLyK1Izh5dmgy3gvDNeJMqORkEnEAcJDwx7t_Aqlq2qBGvNQ3vIUURUsEICEMT4lROQSHiLovjNiI321smRy1bvaAKYAhzaXgGCU9Y0GkSBghhmABDWoikBU-qyGkDAoCGCmwYllZs2JxvWPS5Dkq8mV5YPrExc6ExPbMPlAesEX3FDO8rZgpyug3zIb13MKJDl-EdugyeSFbHoWmWWsmIF8CGvwA26MpVh0UrbE5gs34brgK96M9leH8uo2iYDtM5fDjYWBKzEpmVwOzJYQDHVUom9o_i-wetgu_ubNuLihGdsYJEWFSMpjP9L0F42AlV1-Jw0PxwQP_7sbmAgdmIrKIi1LwixFinsT0fO5lTi5ya57SxMkj5rMjHrwLoyR53Goy0l6SnjNiiJpd6CoMl75v2j6GM8dpNVVC1QuWNqBkNrxnRaWxmxUm8omrkfciMcYtGCeo8zD4MtKP1Im0gUWcYJzUQbpvrfpx2l-467h6bRpzZVhx7lh97Vr9yD0172l-HsVlrIiuOQ8uPQ9z3PrZfm8PHywA7C4lYHJCCO726uSie2mlK4r-k7SlJWDbUFs1YD_1zQiXqCMvrCIsxFI9DWNaf2tTf0YoBFFYIoECN00Jw33QdFmyi_zuvaSzGawa2tp5ux42J2f0-KUCJBSi-APIerJYfLvrR8wrMosK59M-vAXRTsGfOzUsSNCJ2Dh87Y1HXhF3XcajCNq9N2MTOMUJ0S0lneKGzp_SS3IruNJZ3p7Hk2hof0tLfRSL-Dv_Wyxh1evOpEvSFFzvYa4Hb4MaqqRYf7EVHZs_cMmRaazz9PV4raL4mYkMhy4aS5UVI5i3e0IZJcv7cvHBahjDsRQhK2Is19AyY76yqy2WAiJS6AQsrvmXjfQVIwlwJlbQu0Qxsz-M0LO-ZSmFRIgmT2aFwuFqE_e51Xz3NuVDEZ3QACXvcjwvczZTG9T7qdEJIR_5c8hHlbEZHjDXdUfOXyYIDB0r4UwrN5UpZ-sOoQovHE5pnNrgBgHjYoC35It4nZRixDMOXgdt3iLm9KeVvK8aKxVi-GHT2qrqun9JWcSIVeyWS430zeVfD7SBcMHXt9BIdaueZdKidM5fOpfUFBgrsu6r-TI4uu3eh3dGNDG9H3s-jXAHNR7mChP1-TE-yf-mq529t4lJS4aos-SIorUCYy-10XbidgFwk5PsMt3ShplfYJ39bpcXNneI3d0rld9eWc8P7kQWMSJrzpNDYkFUlTJxzLcxGJbav4tsXA5V_6feghu8JORJOsYkV38Ro-g3_-O_xegr_b_du0RJJ-4oGoeINQoVbsWC79d31FtD0Tf0obtEUv0VTaNs898Pnj5BdSzhKVaKRo3gjRxkKxewxWIDNmKREU0fxpo7Clf_OOdZPzeHaNSmr2AC89zDl9Amsv4Rt5K6uOhh7yQmQkMqHJMx6pehIvcETG1yuwMKIlislHKqThLEqdImbLprVqUsfiXk7AiTMjVJYvDFHTdCbEGI-du0luqICOX-tBBLuLqjAIzQalmkFSSxcBBXMMVrQlSWaUTA0F5GrJOXpQMLkP_I5Xku_ju8qvownOZ_sCCRcXoVcm4jwBfwGTlFShZy3bknC5Sqw-M3rF0tJ6p_oVgkIhCQGQcLeKhW5QefrKuw8my-0jx9fTvs-uiRDFD8eQMIMsIxU2EybS5e3maC1SMJS093FdepxS5Z6pBJCovQcZV5mxdx5LejzU3TFQhChBYKEu7_W0QgJ24svSTILQAjX1pobIPBnO6dMPFUIIDLyHqV49BBa8NaYbX2_Bkl8QLXoA8ocQ8Bew958kJFUzFhFSGm_Yvl8Puq-xwCDLykiycDhlJiIR_EeDei8EwzVK662zWEHWkhI8UF4ybFB8OPBVffSdy_H2K4mmegUxKy1YReaobnXh7k17zAUsN-NEo7JYNqyA2aK2YXV63VjMU1Duwdj8n3Eb_jUZSRZDggYgdBrPxD_v9z5g94Z4CT3ZXcO-5m5Hyb-hB0ZKGFy_oVdOWrQL-14DRqT-g1PWG83e_2wo0yOv17n0R_0Sz4dIEjYbHfGGHtf6If-PB-C8w0vwPgNL0jYSekp0-IlnoFedNvn7niDHYVD4ye6JPjxqb9N8bkhAhjeEAEJm7kSSd_Ydn_s9tdTnKoyk7YTRcZ5Z2jyGPjzj2r376GZ-2hJE7wDSLKsYJ5R4_1UJ44eJGHrhRKmAfMCz0X-BU7-gsn949BGGSRQzjceSJjDkaDOQH__8Xpo-x1k5oyGiVWCKyRIGDatMKL7fwRFBSHdoKjeknPOmQHIM4OEG4AaVSDHRkJhHGpG36F_F0zKHys4XjxAKk7IoLnbw5ny-Zg6ieWik1jOTnhM7fbvNN__A-Z7PKv5rG4kYQICvMU2_b4PFstlAs4fhuo5riah-KgAkMS04NkPWhGa4H9Vv1TD7qfpJczHhPcOW_DeJcvqlipHh4g_vl6EQb6P3Y-QVndWXUSx1UUJo6pdiSkIvu-7oC9_6sKcnGtlkPJaGSTMlNQZBuv-ByjhGjnfXWAwzNcTBPGzEyTMqWXpManVM7B-3Fdjs0PS-eklQPjTS5CwNcXr9u-QifJgBlN8pBiWUO9-aI9tdNOMP5HqXfI3zUFS0O4LSnlX92FLfz4mrSFEG6GEUy0GT8K-r7quRb38Ei9B_MkXSdikoOWrEYS6Bb7_XXuqjs3HU4VbRsy0PEbe5vgrKSEo5ysWVDieY9bB6g5LdJ9WnAD8mT5IeEY398C83BeqlNeJvI7n9XiOhImaw04srPYytxe5-VbAUTfBKtPJrMI4QwlzZKA0ujdVkDL83J9wC8lyE5Q_PgAJy61ssvsVqZWVqJVlqdHL_TK-1E9SGxNKorVsaxg8fx4v7dBOIquRgp5Awh3LWI95AqrxCWaIQAso4XQmSBhaV-DswwROjcQKIJ4VJByrQ9NtrFu4jHqUGxeAArPLMp75dkkMW6ZWHmhOyGJGEiaqLKPwfkwvOmD4GxwlDlULLTOPLcuEgH6SMLFglrxpn8OCzFcWEXwUmOV8acPc9nguPE795SNsyKQRQUheUYKEC4VSeO_32A_NeZR6jmBC2JMybHQO5XIFj6clHUqFqzoue2vpTIZ7yLGPIhVF9UA_YPe7KOFKcDmFxR8xdcaMNuzPb3-swz5yqN5H5TjeNZIkjF90Tq6mr6ONrz_BeO_onHM6LZT1uI5ML5cGMlKFlXR-DAlS_hgSJMy4KDwuoJDVc0mHUn44gIQbDiVF7wx9-N5zPBZK4YQUJZxtalA3fne4Gbrfsg-nXwm2apCw5lSpbEarUX-ILwRQIrBZRqHDnwu6eYHgA3pF4rX-72PiQiQueOKSvCCqepVW8ApHCbNf0XQtMj1dT_szuEWPn5upfoqDmLV0LYIShtVof4sVulzhFv_A7IEAw5OChCM1uPxc4MgLjN6E-31EboQjBJQwrhzBpEfP8EB-Z2TbmKC8RwdIeG6D7llNA_PsG_iNyG9YfgxmODYjLveb9HxgA0l4enQZCTb2N3CLTeP5pvG32-spGMbfQG9Fes5BB96zwF4NlsVuWUj6l7iwIsuFwgpmL41_pgR5_Th-XBYWtV9aUimWVPIlQav11ykiTTityCk0FcbxNJDhGW39t6pPfd99rNCpWfoALxbm2cJy0jphSnycevEbcvEbcv4bMNx_hVCI90cJ59hk8eChrg7VF0jZ2nz99drG_k2WP3UgyXKFzHWJQ_K5HZrHIdgZTEUJJL1twow9WELx2GkM6gVDPekog3pvfpb9Pl6RpWM9kHClaHJNO7e3F2bqJgnu1vz9IUl4xuLOCD7zcI8UuVcQRiQteNIyqibTxAgSWYWPJzV4aqGmDT1vwjWBEnkVz6tv78jcbiOXjFpk1DyjuYVQf-nbscUnO-JOe58UYMQCDFeApfSqYav2WVTXBBN4LXdoZJRD379zO1GoQ9IQIOb5QMIdcFMsOSzqeHC8uYLRT4Sjbi7APPy5wKSuoa67sZk-Xi9RlUEq0IX_Y-nszfXl9njDohW0cGlAEo5S37JjH46sKUYIgVLn7GFhhrnFYBMypi6vJBUOCzPPtaHJ0Vz80z_--7cWXsQK4zZ2-QSAwJh7rudNgd98ac4YmPdcjU_slwNOIC6YLy-t9xRKdj8mhUu7BTHhBFdBzxG7jDyTx7b70gyXHg52GV6E8fvQjPNRDttsd_OnbatgmISm7VleL8wtkrAPeGSvd-h1P7MW4gc8Mic94JFxpJp0bCDtPrOMWtCuJFluw8N_sZp92NmEgXoeH5u5TSYsjfQzdluOEq6coCvRfJqqTuo9Qgm0QcLSYnaI13Hcnj8LvMLjIyhhrtSyslTEW7dc3xGCv0kDCRfVborsNS8GQ4hyIWLdcOm6SkgUdes6ZlOKYn6rCxKOz-J59mOo2DcZSPQLoQjLRe2WMLtvVf42fsEFAiXMFth5dDp_vl-EjbebsMUGGJD8BhgkPLXDgLUrvEmwxutEXuYo2t5coMPmd6x7iZdgfL4o1u85dzm9oVTVwwukntlubvoJb6vn3LNK8GdKGHeuqytd2HxTKcImAyWcayF5Pk5PTT80J6GFCCZ4GHIekGAUoWG5r4bPbxWP7SnJsAQJ43iUF5iCfKyGYyU3AeF4JySQMIvULdTzsbv2ME7AzWu7qeln_KKFoZ_MYkhp1sA_shkqrlUII6yEXJY1hS6MMBJ_vVZD03XSGCegoKULxs7GRYGya38mC4apL4HENcXya4q-scJbN-Mk8VpxrbJsO3jKj1qNTXv-hv6jXwhF-IzzBMkKjPX7yz_-X_3UhVJWyBErLGAFE_4H6xoGidfV-Us1sm2CEGlR1KwXa4Zp75_aQ8MyIkDwNM0yzTOaiDHxCQW5SMiuWR53HJtGESGF5cpzkb5wsexusSnN8OXmBAApjdoL7MXeJ9fT4oU6f1lW0iupAzwbhyEN83Kiy7LSC14FIOGM_NLm8_Bw9Irh2QksWPoll-HMeo3pf4C9asIifsTTNpFeF8LLeiBh6dFsaqan890jVyb3UkATl-Qm6FUK3BnDchjGXrXvpFYnqKCcFeuKdfMMxND2QA6nFrMnsuDGZ_nKMP2K99BCZ0H2vsfRc6aUu3Tff40NSye9YIoSpuJK45UcRbmlfCTmawgSriE0pkifOX6_Nkj04ZrPkk4SjtbgyWNz_tJ0_SWuI8gEMpPlPBmGnPfd4fYi7Gsd3ye8hcjLnLh6R9ebcG36CK-Dy9TOS83q2KtO9FaDsdu1lzqOFScZn1oUJNwxrsaHNcCBPu1xEgrHt7pk2QzuUsFX8txWEZUR8m-ihL0fxnvCWxxNGjNAcumGmLkhhJteSpXV92PzsWuqR3S8jFkRJF0U-4xnxXtSfJ-S5RMvnpmbnkKXtM-_QFIJhq8U9vMkYYznnJ5_-aV5bsAfIB4uKOUtZ5CwdGjg_h9MnMjQmVyiM5xpbxwuIZe2xhu_sWua9MTMFcIpIUjYg60svz93txuq-nNynpVJq5xnFETpg0WkMDP2Jf1ekglJIjPubKHIFNooFfo909CGgVOB53gSuMObKCThmRXDnFSZcCIxX2VnX4mn6tKwlXVilJHjA5fwhak3Tqaa_KtSJOEojXaztatKrFOjJTqjeToc5zc6buEijETKjHbIwUmPZATFvZzbJJaSd7LNWGpMVvG2vqatCAAxCkrxjH7OOF33C0YvMnLJSy2F8v1yHV52z09NE0fTWSlODyXsy8h4sPq6KqQfDGLpVWTuWDX8eR6tudA_BJAY2XjNvCiyN8bFZEG5GADKBYUUFLEJGTMuMKUZu4dAPGvBhW3iY84Wc59fKow-WITQIUJ8CNpylCWe0zx2FQXk7W5GVURaCglqUbIkVZm1lAd1GqrUQCEpS4cSZidXWFQTE4QqUQJgioPfjS_jBIdW6Od-TiK_8Wf8pg4kjPVSZGhWEStLShjeggEJt1rqUt8qjxuieKHUpXAIBhIh4vGvoIVn__6QRjp-kEMd_8o0b-hD_0aJ_5w3I_ybb0aQ8M7mesYH_0wczLXoYK45PnLFm_8z4pN87lAi8P01IfyQMn6QKf_KH-_nb5T4z-QsPxfP8nOujppsjtk_oxpq4TAEJWzgm7G7jx__MP-DiwFeJQCvNhi8XQeUudkAFOXcETvs-3VaSTt_nkS7spwBcudNpuZhuw5yGswA-Is1Bq_zMDpn-7S8MMUcgJRzJREo5g1Fv4jieyGh4AyQ69L5GKCK6DPhF_NK5t77BKCKOL4lLDrzz4RfREWALprVAX-xAsC2V1sALXbWLSLZ3j_j_of4O5x1cSi0dSnAJ4CkJZyLGzv8OwWoBKBSgNkqwm0AfLYFKLYAG3XwmdoA5FsM-dpXlFYtWjIBaKvLNYDPvLIrADC21Fpvok1iVhVA2C_q9L3EGKBMnr7jE6uQXJkk6VyiY0It4tnpEkD4xTqDtcUWINaUNpkX1jqbvnGTAOIhB_9OAfkWoNwqIvlMn3yFi8ckBzBbALcByP0GoMi2APkWoNgAlFtFlFtFlFtFqATgkvHgdJa-354CTPoYewqwWwC_ATDZFkBtVDKZOC6dF86YDYArNxoq0Q_OLRhs-ix3CnBbAL9eRKKr8RnqBKA3ALle1w--UOnz0CnAbQCSQcsA7AYgGbQMQKePHKcAt64nfTJoGYDfAJhyC2DTJ31TgF9dceAR3C1AsQUwWwC3AXDZxlc4lT4nmwLsBsAXWwCVvs6aAtZXXnjpNH00NQX4DUCebwGKLcBWHeK5yQAKswVw6aOfKcBvNFQ8N_F9zRigsg2GdPKayEzCRyvTNzBTQLH2Ffii5Eod6IHINQC-9Zi-FxoDfLamH8j6W5k49LLiBkCp9PnKaDsIjx2uqEF6tnBlzSLLa2XA0HuC8dsuel4HegRwDYDv-m0B9DogNdVSALyXtwFwNn2sdb59wCfttgBxHYIpnwL8BiDR1fHCSs_ArRg59LDbihqkd9rSZ15TgEpf6k0BZmVm0ZNoK4OWHjdbKYLeKEvfgIp2avDQ2CoAXgxbBcDbX-sAM99vLgH4TNfKxKFHt1YZ4PmsdYBK5kU8HugXKxqG3qHaAvj17aRKJo5K7Sg93-vd0l7HO9ZkcYfnhmKG0qwzaK-2AHYdEMpcr4PJ1BbAbADybAtQpI8MpYCtOuQbDWXmG1IWMN9v8gCXPrCTAJL95hKgNgE-fbwmASQzy6Q7NaPzLUC5BdBbALtRSZOnD7CkgGILoLaKcOlzJgnAllsAvQXYmDiRKmYBOt8CFFuAcgug1jvLRme9HIPZGDA26ix6wyABbFUy7c102Ccn1viAQwIwawxYqZWvoEcS0sdJEos03oDg63xza7BcjMlo0NJDBOljXokdlQzaZL3AJwLWFxRV6PTxgBRgtgB2C-BWAJQBfw2AOew3iijLLcBWJdVWESpPE8WngHILYDcAiaZd1kFvfUWiBpUpUkC5BbAbALtaSUzzvQKgvN0rAMrDvQbAxNqrAEiVvXJ3QKmv0yTa8QVHHuuH5MqL0k6nGa6jr4Ds0auALOpNFuDXAZCeeRUAyZa3ADZNbZwcDkQLSpkoUvrFKgPkIl5hoFzCKwDKD5ym850XgWl_03y8McDMr0BvKTLnN72QCXelDpTPduFrkbRUZDdTct35xIC0s2l-4zkAc7WmSXjjSthYg2BW0jkAkp6u3AXTL9KkoK-AezbONBVlVElIWZnmlYwWLfhFmhEyYZgbtYuGosSNqQ9KcmEdKQjyDZkv3pBBcQvgtgBbRUSmeQqg_IIbAGU3AHajCJOtM0ASvlUA5NNbB7gs2wKoNQAmqVsDYMq5NHNm1N2QOG6FgTLArQEwp1ua5HGuYjAl2woD5VJbAVBStNSRKFpyIM3ZGgATly1ckeLPKKMDJwpumg1KTCSWJiqLATYaMRyg2ALMzw-WAEy8tQqAJFppSq4YYKIxlzJQNqstgNkA-K0iIm1OWaISgE3zRcWAItKkDEMxPybhAXa9kkVk3XOAfIshOvNeADBX0EpnUdqfFQbK2LMO0Hm-BSi2AGWaDSgFqC2A3gKY9TrY-aLFMEAmmFUGHR0nMwyQmGUDYNebGpKmrAIgDcpad2NWk3WGYrUIyjKS5qeIVG2mVxUI5f1YA2AOj1WAjsbDAkC5NNYBodYbALs2YChZxRoAk0-kKRwiVQx3XqmfaQywkQnCAaJlbwHAlAxpmocU4FYYKEnCGgAzHGwAYh2VACjLwBoAkwasACj4fw3gkgPIJcDHV39pQ1Eg_QoDxcRvAKxeB_hs7SsovHwdUOq1EUWh31sAs7YLQpsldWZODWuXhmrH5mCZ2mplomFKm68DdFFuAHy2BnDxadAtsHX-mS5yVr0FEM13nBBhm8YYRwCgXCmC4l-3AMUqwPmkDjGAQkzXABg1ug4wc0V6i7GJzeLoPmrBgGGaadRnCrCrgDJS5ssiMDRyA2DyNJQ1XvVc5K2eMlAs4hoA4wvT8L_kNMiuFUG_SEMTE8D81p0twrmVQUuxdet1iPTkoi8o8G2VAeLY0pC4FOBXGWx8Mrf8TIgcW2XwkaPosiUxsCsNYI8ARXS-eIspT7yb7TqgnK9Zy0piPFQaoBQpUghkWgtOwF-koVTxqNZg5Dx8eDgO7eHh0zRcmw8Pp2Y4VfDPh7_BjzE90Kn5-eHTDl7Yeqyu3fTzw8_nv4efXarz_-370-svh_56fHr49Fh1Y_jX9XKopuaHtjoO1RsEs1N_31_P08OnMs-Q4-HT3x6-Pnz66MIO-fdhZxe0tyqt_vDwEjDl700RTCflwA3BWf33Dw-_YZl5_nuP_wm6vDQ6jIq__3_majmR?type=png)](https://mermaid.live/edit#pako:eNqNfW2P5LiR5l9J1H5wN9Bt6IWvvQMD9swucAd4MXfj2wVuZ2EolaosTStTOZKyq2sM_6D9D_fNf-wYEVlZIhUhtb1YuCuefEjxJRgkI4J_e6j7Q_Pw6eGx65_rp2qYdn_508_n3a7uqnH8oXncnfvhVHW7x7brPv3TYwH__TBOQ_-5-fRPzrnb__743B6mp0_55es_R78-XttD85dmOL0SPD4WVX0n2Dv3mGUbHM3XqTkfmsNPdX9pbjz1Y1M8lneecm91ZTd49v309FoNVYf_3H9eleW-3PM_r6qpzLKssIVx__nzQ3U4tec2IKup_dLshubSD9P488_nd3Pg-58f_utedkRxa8-Y2avAXPen0_Xc_nptEjqvJDqveDob6C5ddR53724VfJ9QWpHScpRlboBy6OumObTno0QccAJxkLDERRmIp6Z-Ord1GGZcewaMRFqUbAMYaID_TVQfdv-zvw7nqgu_Ox92P_T19dScF10mNojhGsSYDBrkT33_efd9NVVdf4wIQc4TgmRBmDtvMhgDf67O17Ee2su0-9e-a_s3ToJwnCRZcubaldC4XVN9aUKHHavpqRmaw-5UTVMzzDqOoCw3SpbcXueFDtz7MMg-76iEGR-KWT6ULPmMUzYPfEkdd2FOXPpz3F0EZtlRsmAvsrwwRWBvz48gmtr-vIP_xdITmqMnyZJehUaCzvvujW63f9mNl6ZuH9s6lHKegg77w6wM_AlbBkre1OasmFyXzodi_u25GS_VpRloQP-5Ola_ted5-xOUpUcJO6A1Ko1maPsDzMRkOGsrDWfNzw8FDT4GOph47y7XfRdYoeVjjQFAiVkVzKDOvYdGmBPu3h1eJ3U0qAHKD2qQcLXOShiEr2y7Y3MeYmUMCKG6QbIcGkWmiwyGxr2GMDLCgDi0VPX-cRe06uFawz_nIwR_yXYhSrgRkpfWa7UoDUb6jJlQbLugRGTWS-brOa03IUV2vWSn1nPW4hI4hAYPc-jQnOvmlfWOWNLeRVxvOutoVs5Jod5tmI-wIqRNQ78R-jdIuKZBiUc1CxorDMa4vPcJvRfp2RHpHMyjuh3qa1cNu1shMaeTZlCQ8JwwSELlXupuOdWdUyKd4unQNqguoUFlUiOSGp4U-g6VNP_NYjc5x_L5bNZHYdZVhy_t2xB7xUikPuNJi5gUBtZ5SkjF3vF873gTkw4NWIbBAkZtl5CLzerZZvVoZXR9sFy5ZvWZ1Pc-Y_veo124v46wAI08p2QSgoTnhK4fq66RCJ1IuOz70iqaQ3E33XXuGzUhOWqSMNTaarCwwnRvj2eyKxY1JhRPC5Ilrc-8Am14bpvr8y9VNYz7oW2-NPO6IoYlRcmCVBXeKY91fWyGIUzVRUUJwnGSZMlZ6sImgxWWtr6ba-9XHEuMEtZ-cBorG5TpQVjgCSUZD05ztMrAAl8_DWEH15zDRiZsCvvP8fgKGIE0SLjtRq6gEU7NEPbPYWEfmzDAQm9Nfei1eJsRkMI2I0jY7ZFGM-qpvYy_25HRF2-NdCFtjTSnXaw1uIy_NmxYDIP5ESpbhR6LVkJACtRBwq-E1tqCVvGw86LpcCsoZrZSpYOErTQaB8dQz-GMhhnPakVWdk9rHbB-t6QVTBv6iVSGs1Kb4MrzXfO1qa-3I4PttpdWIpCI5cDQ_uUarPcWVuK0vKSAXCyAHePWl3gAEDRdMGsmKIEZjgEl0pY8rRYbR-gCLw5LLw1Lh6tefR2n_jSy7eGkhQ8kXMUd7v_f6h0Y08Zw0hEASHhOWPja06k9rsyegBJp2dMll_tYR5-q4ddrE5PmXiLNPUtazO2pS5XaPQCQGIuMZ8xvjGGQ7Q7Nrq7qpyYlzUXSnCcFhXRqu3aqhhe-PYtC5GS1kSvh08Nyfw3LaPvbSk-VYhOUfBPg9vNSDYewNUyoxA8v-Q8vC6SaFkddQSJS8d-LW_mhOYYdyG2_vZiv8SmgU2IRii9CZ3PdxTamFhtT842pYYZ-l5K-7ojDjBU0TPihWJKRNAyenhyauh2phdJikwaSjlNAwn8MzOHxur_0Yb1IW0acu5qfuyZDstMpVDWxUIJMIjN8MxvQrc9Dmw4zI2pUw2tUsky4_pKWSSeaKE40UZwxuKH-0nbBWL0OvDERUCIzr7sdrI_10J5aOFhYYXbSEhkkPLNGvXhsx64SF3TnxKZgLeHwZ7R-GN5vmCGiGeREM4g29Pu2g-NAptRkgjhxkXP8Iud80kpVnY5IJ84T9kjU0mZZaiJpUIp7aJAIjeMzjXbz-RjWPtAgghIMOJGb7WWfa1pRurYCExcWQcZuCzCJN-d5CyXbzmLLFGLLFGLLFA5b5nqeXnYbO4CAFfnZQeNxvYVLt7qF06stfnER9vwi7EuLtw7BRnqjlrq2tCI5uyR4OmGfwhK_WXFxPfb8euyVJhOHhuImvTh6FD96FB7uNcFk_hZ2sVcV36u4Fj_146UVG1tcfz2__npcf09VELUipxc5efViShx9Y3M98YxGWiqChGfEQ_Sn61A_CYzidxv-u43HI_SIcnuBCD8Ty_HSTLdgleyry9SO4HBQN8ME12dhfCcfYSUTJUjYj6BTCfqG_bULe4z2nHKKM4Q_kvB48PVW2wEWiWmhV60RaQ1Pi6vk9TbKeE5xPlh-Pjho2NBRONsEUie2qePb9HbjuRgYovJ3ovJ3ovJ3b-P5OeyKmvP4u7Cu42qQ1l8c2I4f2Hh0f2j7uhkrfvvmvTgmPD8m0I0jLLZ9_SRqCdGZw_POHN7T7crQjk_iuaL34jhj7wFchqbNWD_1PVtPAPCMIOEZPZ6xDEMLV1UJmRfJPEuW4z1se-n6U5VULM8lrjznuaCnH6tQq4kzfgAgMhY8IzTecagOzfL4GKQiHd9yOR11g7fKrq4WPSHZZiBh-QoYMeNL11X7NqYqjERV8MMEra_pqUm2iSAQmRzP5LFHxzGodTpGSAjFIVLwQ6S8-SuMaKJw_SpZVCBhKRUqyurUdvxAUZlEqDKesCCvqce7Vc_SiuOPs86Us3j21nx9avetcPiEIJYVJTxr8ca6IyeklLIQKZmKwmk-WjgVrje7xTBCAMuIEsb5oyxwM9yQ1bv4bALwLh8gWTKWhk63-sdHOnU4LN3DCMS7NBjuQCv82WcwOv_U7juumigXCINkSahyg-fv94vWJSdCWE6ULDl1kRXF_eIebhgf53woZvlQwvIphXXELT7RLjf3hJOIFePHZpTFXj_3Yfsq9RGCeJ8wkDCs2mB1w9Ac2kkw6wnF04JkSWsLq-ObgSUpYlhSlDD-a9qjahoasILoDL8JtZ47rQGEd1oDyZJTm1zj1npmZpO3AdiHw8vuXXTrOOtB-ilbFkqWZZnC4JJZhw_YdYF-7quGQpYNJTwbjIc_N4cWeq86N8GCu4QfJq6jhBSpNUdNdzDNeei7jvyc5HZAtEDP3cUUpizw3ATqWR2D8QCnYXNCkPOEIGEJ0UQem2p5n09SiY4xi8u8yHAHWYUhMU7gKj3X1yRmfQ5QwvOhz3Sw30NX1dPvRpbUiaSOJyVHhqlqO94kJpDI6llW3H-GCdY89WFPno5TQkiUzMYT_5zfXRWXeoAAImPOM9IFO54u99HoIalIV_B0sKp8aXDC8xUsRcaSZ8TrgKrrdsH8bBYVVCKd4ukMOWSGHgbNz9uPBBSZDc9sSfufFjYZSUU6ZqD7PM_dmws_mmSLbTaheJ8dkCz9a3Jr0WenqsNW4xTGkPD9BGQdbFDCeAOVBerQOhiQv4VtdVBxwoELQXmvIJAw3KrI7ey-_dCEXw2LOiOM5wUJw2s17mzut7mhNSBi5RhXF1A8LUg4WoP-Yb9cD8dTdItNIoHLMA5hqszoJjOY_PvQjHMXqEy4wCQJQ5U7XPNDf4Oj4nJ2EoKnBAlDqXJNN3_DAAE1A2dJEYqnBQlHq3B1n6qvqU4imUCmmMVdlcGgBp303dScwIkodHPVXZ6CKpkwPgS08ifmyPgP80KBgy8UJNxhk9Laleh2-HKujv3xyjU4YlhelCw_Bv6M58b9-KvI6EVG9tRY0c3LNx_FKvHSRYmXLvrmLHvkjW1CCKyadZW1JZ4XTkMFG61d6MvPTRrlIx4QlqzfsdUlHsG2h92-PyfHbEEm1a9kD141nt1B7Q7Vl3bxtUr8Wr5q_tWMqrvm5nI684pLyK1Izh5dmgy3gvDNeJMqORkEnEAcJDwx7t_Aqlq2qBGvNQ3vIUURUsEICEMT4lROQSHiLovjNiI321smRy1bvaAKYAhzaXgGCU9Y0GkSBghhmABDWoikBU-qyGkDAoCGCmwYllZs2JxvWPS5Dkq8mV5YPrExc6ExPbMPlAesEX3FDO8rZgpyug3zIb13MKJDl-EdugyeSFbHoWmWWsmIF8CGvwA26MpVh0UrbE5gs34brgK96M9leH8uo2iYDtM5fDjYWBKzEpmVwOzJYQDHVUom9o_i-wetgu_ubNuLihGdsYJEWFSMpjP9L0F42AlV1-Jw0PxwQP_7sbmAgdmIrKIi1LwixFinsT0fO5lTi5ya57SxMkj5rMjHrwLoyR53Goy0l6SnjNiiJpd6CoMl75v2j6GM8dpNVVC1QuWNqBkNrxnRaWxmxUm8omrkfciMcYtGCeo8zD4MtKP1Im0gUWcYJzUQbpvrfpx2l-467h6bRpzZVhx7lh97Vr9yD0172l-HsVlrIiuOQ8uPQ9z3PrZfm8PHywA7C4lYHJCCO726uSie2mlK4r-k7SlJWDbUFs1YD_1zQiXqCMvrCIsxFI9DWNaf2tTf0YoBFFYIoECN00Jw33QdFmyi_zuvaSzGawa2tp5ux42J2f0-KUCJBSi-APIerJYfLvrR8wrMosK59M-vAXRTsGfOzUsSNCJ2Dh87Y1HXhF3XcajCNq9N2MTOMUJ0S0lneKGzp_SS3IruNJZ3p7Hk2hof0tLfRSL-Dv_Wyxh1evOpEvSFFzvYa4Hb4MaqqRYf7EVHZs_cMmRaazz9PV4raL4mYkMhy4aS5UVI5i3e0IZJcv7cvHBahjDsRQhK2Is19AyY76yqy2WAiJS6AQsrvmXjfQVIwlwJlbQu0Qxsz-M0LO-ZSmFRIgmT2aFwuFqE_e51Xz3NuVDEZ3QACXvcjwvczZTG9T7qdEJIR_5c8hHlbEZHjDXdUfOXyYIDB0r4UwrN5UpZ-sOoQovHE5pnNrgBgHjYoC35It4nZRixDMOXgdt3iLm9KeVvK8aKxVi-GHT2qrqun9JWcSIVeyWS430zeVfD7SBcMHXt9BIdaueZdKidM5fOpfUFBgrsu6r-TI4uu3eh3dGNDG9H3s-jXAHNR7mChP1-TE-yf-mq529t4lJS4aos-SIorUCYy-10XbidgFwk5PsMt3ShplfYJ39bpcXNneI3d0rld9eWc8P7kQWMSJrzpNDYkFUlTJxzLcxGJbav4tsXA5V_6feghu8JORJOsYkV38Ro-g3_-O_xegr_b_du0RJJ-4oGoeINQoVbsWC79d31FtD0Tf0obtEUv0VTaNs898Pnj5BdSzhKVaKRo3gjRxkKxewxWIDNmKREU0fxpo7Clf_OOdZPzeHaNSmr2AC89zDl9Amsv4Rt5K6uOhh7yQmQkMqHJMx6pehIvcETG1yuwMKIlislHKqThLEqdImbLprVqUsfiXk7AiTMjVJYvDFHTdCbEGI-du0luqICOX-tBBLuLqjAIzQalmkFSSxcBBXMMVrQlSWaUTA0F5GrJOXpQMLkP_I5Xku_ju8qvownOZ_sCCRcXoVcm4jwBfwGTlFShZy3bknC5Sqw-M3rF0tJ6p_oVgkIhCQGQcLeKhW5QefrKuw8my-0jx9fTvs-uiRDFD8eQMIMsIxU2EybS5e3maC1SMJS093FdepxS5Z6pBJCovQcZV5mxdx5LejzU3TFQhChBYKEu7_W0QgJ24svSTILQAjX1pobIPBnO6dMPFUIIDLyHqV49BBa8NaYbX2_Bkl8QLXoA8ocQ8Bew958kJFUzFhFSGm_Yvl8Puq-xwCDLykiycDhlJiIR_EeDei8EwzVK662zWEHWkhI8UF4ybFB8OPBVffSdy_H2K4mmegUxKy1YReaobnXh7k17zAUsN-NEo7JYNqyA2aK2YXV63VjMU1Duwdj8n3Eb_jUZSRZDggYgdBrPxD_v9z5g94Z4CT3ZXcO-5m5Hyb-hB0ZKGFy_oVdOWrQL-14DRqT-g1PWG83e_2wo0yOv17n0R_0Sz4dIEjYbHfGGHtf6If-PB-C8w0vwPgNL0jYSekp0-IlnoFedNvn7niDHYVD4ye6JPjxqb9N8bkhAhjeEAEJm7kSSd_Ydn_s9tdTnKoyk7YTRcZ5Z2jyGPjzj2r376GZ-2hJE7wDSLKsYJ5R4_1UJ44eJGHrhRKmAfMCz0X-BU7-gsn949BGGSRQzjceSJjDkaDOQH__8Xpo-x1k5oyGiVWCKyRIGDatMKL7fwRFBSHdoKjeknPOmQHIM4OEG4AaVSDHRkJhHGpG36F_F0zKHys4XjxAKk7IoLnbw5ny-Zg6ieWik1jOTnhM7fbvNN__A-Z7PKv5rG4kYQICvMU2_b4PFstlAs4fhuo5riah-KgAkMS04NkPWhGa4H9Vv1TD7qfpJczHhPcOW_DeJcvqlipHh4g_vl6EQb6P3Y-QVndWXUSx1UUJo6pdiSkIvu-7oC9_6sKcnGtlkPJaGSTMlNQZBuv-ByjhGjnfXWAwzNcTBPGzEyTMqWXpManVM7B-3Fdjs0PS-eklQPjTS5CwNcXr9u-QifJgBlN8pBiWUO9-aI9tdNOMP5HqXfI3zUFS0O4LSnlX92FLfz4mrSFEG6GEUy0GT8K-r7quRb38Ei9B_MkXSdikoOWrEYS6Bb7_XXuqjs3HU4VbRsy0PEbe5vgrKSEo5ysWVDieY9bB6g5LdJ9WnAD8mT5IeEY398C83BeqlNeJvI7n9XiOhImaw04srPYytxe5-VbAUTfBKtPJrMI4QwlzZKA0ujdVkDL83J9wC8lyE5Q_PgAJy61ssvsVqZWVqJVlqdHL_TK-1E9SGxNKorVsaxg8fx4v7dBOIquRgp5Awh3LWI95AqrxCWaIQAso4XQmSBhaV-DswwROjcQKIJ4VJByrQ9NtrFu4jHqUGxeAArPLMp75dkkMW6ZWHmhOyGJGEiaqLKPwfkwvOmD4GxwlDlULLTOPLcuEgH6SMLFglrxpn8OCzFcWEXwUmOV8acPc9nguPE795SNsyKQRQUheUYKEC4VSeO_32A_NeZR6jmBC2JMybHQO5XIFj6clHUqFqzoue2vpTIZ7yLGPIhVF9UA_YPe7KOFKcDmFxR8xdcaMNuzPb3-swz5yqN5H5TjeNZIkjF90Tq6mr6ONrz_BeO_onHM6LZT1uI5ML5cGMlKFlXR-DAlS_hgSJMy4KDwuoJDVc0mHUn44gIQbDiVF7wx9-N5zPBZK4YQUJZxtalA3fne4Gbrfsg-nXwm2apCw5lSpbEarUX-ILwRQIrBZRqHDnwu6eYHgA3pF4rX-72PiQiQueOKSvCCqepVW8ApHCbNf0XQtMj1dT_szuEWPn5upfoqDmLV0LYIShtVof4sVulzhFv_A7IEAw5OChCM1uPxc4MgLjN6E-31EboQjBJQwrhzBpEfP8EB-Z2TbmKC8RwdIeG6D7llNA_PsG_iNyG9YfgxmODYjLveb9HxgA0l4enQZCTb2N3CLTeP5pvG32-spGMbfQG9Fes5BB96zwF4NlsVuWUj6l7iwIsuFwgpmL41_pgR5_Th-XBYWtV9aUimWVPIlQav11ykiTTityCk0FcbxNJDhGW39t6pPfd99rNCpWfoALxbm2cJy0jphSnycevEbcvEbcv4bMNx_hVCI90cJ59hk8eChrg7VF0jZ2nz99drG_k2WP3UgyXKFzHWJQ_K5HZrHIdgZTEUJJL1twow9WELx2GkM6gVDPekog3pvfpb9Pl6RpWM9kHClaHJNO7e3F2bqJgnu1vz9IUl4xuLOCD7zcI8UuVcQRiQteNIyqibTxAgSWYWPJzV4aqGmDT1vwjWBEnkVz6tv78jcbiOXjFpk1DyjuYVQf-nbscUnO-JOe58UYMQCDFeApfSqYav2WVTXBBN4LXdoZJRD379zO1GoQ9IQIOb5QMIdcFMsOSzqeHC8uYLRT4Sjbi7APPy5wKSuoa67sZk-Xi9RlUEq0IX_Y-nszfXl9njDohW0cGlAEo5S37JjH46sKUYIgVLn7GFhhrnFYBMypi6vJBUOCzPPtaHJ0Vz80z_--7cWXsQK4zZ2-QSAwJh7rudNgd98ac4YmPdcjU_slwNOIC6YLy-t9xRKdj8mhUu7BTHhBFdBzxG7jDyTx7b70gyXHg52GV6E8fvQjPNRDttsd_OnbatgmISm7VleL8wtkrAPeGSvd-h1P7MW4gc8Mic94JFxpJp0bCDtPrOMWtCuJFluw8N_sZp92NmEgXoeH5u5TSYsjfQzdluOEq6coCvRfJqqTuo9Qgm0QcLSYnaI13Hcnj8LvMLjIyhhrtSyslTEW7dc3xGCv0kDCRfVborsNS8GQ4hyIWLdcOm6SkgUdes6ZlOKYn6rCxKOz-J59mOo2DcZSPQLoQjLRe2WMLtvVf42fsEFAiXMFth5dDp_vl-EjbebsMUGGJD8BhgkPLXDgLUrvEmwxutEXuYo2t5coMPmd6x7iZdgfL4o1u85dzm9oVTVwwukntlubvoJb6vn3LNK8GdKGHeuqytd2HxTKcImAyWcayF5Pk5PTT80J6GFCCZ4GHIekGAUoWG5r4bPbxWP7SnJsAQJ43iUF5iCfKyGYyU3AeF4JySQMIvULdTzsbv2ME7AzWu7qeln_KKFoZ_MYkhp1sA_shkqrlUII6yEXJY1hS6MMBJ_vVZD03XSGCegoKULxs7GRYGya38mC4apL4HENcXya4q-scJbN-Mk8VpxrbJsO3jKj1qNTXv-hv6jXwhF-IzzBMkKjPX7yz_-X_3UhVJWyBErLGAFE_4H6xoGidfV-Us1sm2CEGlR1KwXa4Zp75_aQ8MyIkDwNM0yzTOaiDHxCQW5SMiuWR53HJtGESGF5cpzkb5wsexusSnN8OXmBAApjdoL7MXeJ9fT4oU6f1lW0iupAzwbhyEN83Kiy7LSC14FIOGM_NLm8_Bw9Irh2QksWPoll-HMeo3pf4C9asIifsTTNpFeF8LLeiBh6dFsaqan890jVyb3UkATl-Qm6FUK3BnDchjGXrXvpFYnqKCcFeuKdfMMxND2QA6nFrMnsuDGZ_nKMP2K99BCZ0H2vsfRc6aUu3Tff40NSye9YIoSpuJK45UcRbmlfCTmawgSriE0pkifOX6_Nkj04ZrPkk4SjtbgyWNz_tJ0_SWuI8gEMpPlPBmGnPfd4fYi7Gsd3ye8hcjLnLh6R9ebcG36CK-Dy9TOS83q2KtO9FaDsdu1lzqOFScZn1oUJNwxrsaHNcCBPu1xEgrHt7pk2QzuUsFX8txWEZUR8m-ihL0fxnvCWxxNGjNAcumGmLkhhJteSpXV92PzsWuqR3S8jFkRJF0U-4xnxXtSfJ-S5RMvnpmbnkKXtM-_QFIJhq8U9vMkYYznnJ5_-aV5bsAfIB4uKOUtZ5CwdGjg_h9MnMjQmVyiM5xpbxwuIZe2xhu_sWua9MTMFcIpIUjYg60svz93txuq-nNynpVJq5xnFETpg0WkMDP2Jf1ekglJIjPubKHIFNooFfo909CGgVOB53gSuMObKCThmRXDnFSZcCIxX2VnX4mn6tKwlXVilJHjA5fwhak3Tqaa_KtSJOEojXaztatKrFOjJTqjeToc5zc6buEijETKjHbIwUmPZATFvZzbJJaSd7LNWGpMVvG2vqatCAAxCkrxjH7OOF33C0YvMnLJSy2F8v1yHV52z09NE0fTWSlODyXsy8h4sPq6KqQfDGLpVWTuWDX8eR6tudA_BJAY2XjNvCiyN8bFZEG5GADKBYUUFLEJGTMuMKUZu4dAPGvBhW3iY84Wc59fKow-WITQIUJ8CNpylCWe0zx2FQXk7W5GVURaCglqUbIkVZm1lAd1GqrUQCEpS4cSZidXWFQTE4QqUQJgioPfjS_jBIdW6Od-TiK_8Wf8pg4kjPVSZGhWEStLShjeggEJt1rqUt8qjxuieKHUpXAIBhIh4vGvoIVn__6QRjp-kEMd_8o0b-hD_0aJ_5w3I_ybb0aQ8M7mesYH_0wczLXoYK45PnLFm_8z4pN87lAi8P01IfyQMn6QKf_KH-_nb5T4z-QsPxfP8nOujppsjtk_oxpq4TAEJWzgm7G7jx__MP-DiwFeJQCvNhi8XQeUudkAFOXcETvs-3VaSTt_nkS7spwBcudNpuZhuw5yGswA-Is1Bq_zMDpn-7S8MMUcgJRzJREo5g1Fv4jieyGh4AyQ69L5GKCK6DPhF_NK5t77BKCKOL4lLDrzz4RfREWALprVAX-xAsC2V1sALXbWLSLZ3j_j_of4O5x1cSi0dSnAJ4CkJZyLGzv8OwWoBKBSgNkqwm0AfLYFKLYAG3XwmdoA5FsM-dpXlFYtWjIBaKvLNYDPvLIrADC21Fpvok1iVhVA2C_q9L3EGKBMnr7jE6uQXJkk6VyiY0It4tnpEkD4xTqDtcUWINaUNpkX1jqbvnGTAOIhB_9OAfkWoNwqIvlMn3yFi8ckBzBbALcByP0GoMi2APkWoNgAlFtFlFtFlFtFqATgkvHgdJa-354CTPoYewqwWwC_ATDZFkBtVDKZOC6dF86YDYArNxoq0Q_OLRhs-ix3CnBbAL9eRKKr8RnqBKA3ALle1w--UOnz0CnAbQCSQcsA7AYgGbQMQKePHKcAt64nfTJoGYDfAJhyC2DTJ31TgF9dceAR3C1AsQUwWwC3AXDZxlc4lT4nmwLsBsAXWwCVvs6aAtZXXnjpNH00NQX4DUCebwGKLcBWHeK5yQAKswVw6aOfKcBvNFQ8N_F9zRigsg2GdPKayEzCRyvTNzBTQLH2Ffii5Eod6IHINQC-9Zi-FxoDfLamH8j6W5k49LLiBkCp9PnKaDsIjx2uqEF6tnBlzSLLa2XA0HuC8dsuel4HegRwDYDv-m0B9DogNdVSALyXtwFwNn2sdb59wCfttgBxHYIpnwL8BiDR1fHCSs_ArRg59LDbihqkd9rSZ15TgEpf6k0BZmVm0ZNoK4OWHjdbKYLeKEvfgIp2avDQ2CoAXgxbBcDbX-sAM99vLgH4TNfKxKFHt1YZ4PmsdYBK5kU8HugXKxqG3qHaAvj17aRKJo5K7Sg93-vd0l7HO9ZkcYfnhmKG0qwzaK-2AHYdEMpcr4PJ1BbAbADybAtQpI8MpYCtOuQbDWXmG1IWMN9v8gCXPrCTAJL95hKgNgE-fbwmASQzy6Q7NaPzLUC5BdBbALtRSZOnD7CkgGILoLaKcOlzJgnAllsAvQXYmDiRKmYBOt8CFFuAcgug1jvLRme9HIPZGDA26ix6wyABbFUy7c102Ccn1viAQwIwawxYqZWvoEcS0sdJEos03oDg63xza7BcjMlo0NJDBOljXokdlQzaZL3AJwLWFxRV6PTxgBRgtgB2C-BWAJQBfw2AOew3iijLLcBWJdVWESpPE8WngHILYDcAiaZd1kFvfUWiBpUpUkC5BbAbALtaSUzzvQKgvN0rAMrDvQbAxNqrAEiVvXJ3QKmv0yTa8QVHHuuH5MqL0k6nGa6jr4Ds0auALOpNFuDXAZCeeRUAyZa3ADZNbZwcDkQLSpkoUvrFKgPkIl5hoFzCKwDKD5ym850XgWl_03y8McDMr0BvKTLnN72QCXelDpTPduFrkbRUZDdTct35xIC0s2l-4zkAc7WmSXjjSthYg2BW0jkAkp6u3AXTL9KkoK-AezbONBVlVElIWZnmlYwWLfhFmhEyYZgbtYuGosSNqQ9KcmEdKQjyDZkv3pBBcQvgtgBbRUSmeQqg_IIbAGU3AHajCJOtM0ASvlUA5NNbB7gs2wKoNQAmqVsDYMq5NHNm1N2QOG6FgTLArQEwp1ua5HGuYjAl2woD5VJbAVBStNSRKFpyIM3ZGgATly1ckeLPKKMDJwpumg1KTCSWJiqLATYaMRyg2ALMzw-WAEy8tQqAJFppSq4YYKIxlzJQNqstgNkA-K0iIm1OWaISgE3zRcWAItKkDEMxPybhAXa9kkVk3XOAfIshOvNeADBX0EpnUdqfFQbK2LMO0Hm-BSi2AGWaDSgFqC2A3gKY9TrY-aLFMEAmmFUGHR0nMwyQmGUDYNebGpKmrAIgDcpad2NWk3WGYrUIyjKS5qeIVG2mVxUI5f1YA2AOj1WAjsbDAkC5NNYBodYbALs2YChZxRoAk0-kKRwiVQx3XqmfaQywkQnCAaJlbwHAlAxpmocU4FYYKEnCGgAzHGwAYh2VACjLwBoAkwasACj4fw3gkgPIJcDHV39pQ1Eg_QoDxcRvAKxeB_hs7SsovHwdUOq1EUWh31sAs7YLQpsldWZODWuXhmrH5mCZ2mplomFKm68DdFFuAHy2BnDxadAtsHX-mS5yVr0FEM13nBBhm8YYRwCgXCmC4l-3AMUqwPmkDjGAQkzXABg1ug4wc0V6i7GJzeLoPmrBgGGaadRnCrCrgDJS5ssiMDRyA2DyNJQ1XvVc5K2eMlAs4hoA4wvT8L_kNMiuFUG_SEMTE8D81p0twrmVQUuxdet1iPTkoi8o8G2VAeLY0pC4FOBXGWx8Mrf8TIgcW2XwkaPosiUxsCsNYI8ARXS-eIspT7yb7TqgnK9Zy0piPFQaoBQpUghkWgtOwF-koVTxqNZg5Dx8eDgO7eHh0zRcmw8Pp2Y4VfDPh7_BjzE90Kn5-eHTDl7Yeqyu3fTzw8_nv4efXarz_-370-svh_56fHr49Fh1Y_jX9XKopuaHtjoO1RsEs1N_31_P08OnMs-Q4-HT3x6-Pnz66MIO-fdhZxe0tyqt_vDwEjDl700RTCflwA3BWf33Dw-_YZl5_nuP_wm6vDQ6jIq__3_majmR)

## Accessing the catalog  
You can access the catalog using any standard IIIF Viewer including Mirador 3.0 and yet better free instances of it hosted in the
<a href="https://iiif.biblissima.fr/mirador3/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/IIIF2Collection.json" target="_blank">Mirador in Biblissima</a>.
![Screenshot](https://pbs.twimg.com/media/GmPDuFSbwAAR8O0?format=jpg&name=small "IIIFDexir")

## Important Notes

I aim to keep the catalog healthy despite daily changes in its structure and contents. As it expands, I make necessary modifications for enrichment. The final goal is a machine-readable catalog to present statistics and analytical information. Some resources reference external sources via the "seeAlso" field, which needs parsing. It's crucial to associate resources with controlled vocabularies like Getty's AAT and TGN, and the Library of Congress's TGM and SH.

## Preparing KG 
Creating a Knowledge Graph from the IIIFDexir is straightforward. IIIF Collections and Manifests are in JSON-LD format, but we used the Turtle format to implement a simple ontology for Data visualizatio representation. The primary entities are ResourceCollection (IIIF Collection) and DigitalResource (IIIF Manifest), both represented by owl:Class.

## Ontology
```turtle
                    
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix so: <https://schema.org/> .
@prefix stardog: <tag:stardog:api:> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix : <http://api.stardog.com/> .
@prefix aat: <https://vocab.getty.edu/aat/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix dc: <http://purl.org/dc/elements/1.1/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix mdhn: <http://example.com/mdhn/> .
@prefix wd: <https://www.wikidata.org/wiki/> .
@prefix tgm: <http://id.loc.gov/vovabulary/graphicMaterials/> .
@prefix tgn: <http://vocab.getty.edu/tgn/> .
@prefix fhkb: <http://www.example.com/genealogy.owl#> .
@prefix lcsh: <https://id.loc.gov/authorities/subjects/> .

mdhn:ResourceCollection a owl:Class ;
    rdfs:comment "A collection of IIIF resources that contain manifests and nested collections." ;
    rdfs:label "Resource Collection" .

mdhn:DigitalResource a owl:Class ;
    rdfs:comment "A IIIF manifest representing a digital resource such as a book, photograph, or video." ;
    rdfs:label "Digital Resource" .

mdhn:Creator a owl:Class ;
    rdfs:comment "An entity responsible for creating the digital resource." ;
    rdfs:label "Creator" .

mdhn:AATTerm a owl:Class ;
    rdfs:comment "Root Class for all AAT inherited concepts" ;
    rdfs:label "AATTerm";
     rdfs:subClassOf  mdhn:SubjectSource  .

mdhn:AATSubject a owl:Class ;
    rdfs:comment "Classes choosed as AAT subset for Subjects and it is used to associate AATs as Topical headings to the photographs" ;
    rdfs:label "AATSubject" ;
    rdfs:subClassOf mdhn:AATTerm .

mdhn:ScriptStyleType a owl:Class ;
    rdfs:comment "Classes choosed as a small AAT subset and it is used to determine the script style of all kinds of calligraphy resources." ;
    rdfs:label "Script Style Type" ;
    rdfs:subClassOf mdhn:AATTerm .

mdhn:ResourceType a owl:Class ;
    rdfs:comment "Classes choosed as a AAT subset and it is used as First Level Classification of all resources." ;
    rdfs:label "Resource Type" ;
    rdfs:subClassOf mdhn:AATTerm .

mdhn:DocumentGenre a owl:Class ;
    rdfs:comment "Classes choosed as a subset and it is used as Second Level classification of document resources." ;
    rdfs:label "Document Genre" ;
    rdfs:subClassOf mdhn:AATTerm .

mdhn:DepartedCollection a owl:Class ;
    rdfs:comment "The class for integrating departed folios as logical collection into a single virtual collection" ;
    rdfs:label "Departed Collection" .

mdhn:Publisher a owl:Class ;
    rdfs:comment "An entity responsible for publishing or making the resource available." ;
    rdfs:label "Publisher" .

mdhn:ICSubjectSource a owl:Class ;
    rdfs:comment "Iconography subjects source based on WikiData" ;
    rdfs:label "ICSubjectSource" .    

mdhn:CanvasType a owl:Class ;
    rdfs:comment "The type of canvas used within a IIIF manifest to represent a resource page or image." ;
    rdfs:label "Canvas Type" .

mdhn:LCTGMSubject a owl:Class ;
    rdfs:comment "Classes to associate Theasures Of Graphical Material subjects to the photographs" ;
    rdfs:label "LCTGMSubject" ;
    rdfs:subClassOf mdhn:SubjectSource .

mdhn:LCSHSubject a owl:Class ;
    rdfs:comment "Classes to associate LC Subject Headings to the photographs" ;
    rdfs:label "LCSHSubject" ;
    rdfs:subClassOf mdhn:SubjectSource .

mdhn:GettyTGN a owl:Class ;
    rdfs:comment "Getty TGN Class for Geographic Places" ;
    rdfs:label "GettyTGN" .

mdhn:AgentialInfo a owl:Class ;
    rdfs:comment "Agential info based on FHKB and references to wikidata when possible" ;
    rdfs:label "AgentialInfo" ;
    rdfs:subClassOf fhkb:Person .



mdhn:TemporalInfo a owl:Class ;
    rdfs:comment "First try to support temporal entity type" ;
    rdfs:label "TemporalInfo" .

mdhn:hasCreator a owl:ObjectProperty ;
    rdfs:comment "Links a DigitalResource to its creator." ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "has creator" ;
    rdfs:range mdhn:Creator .
mdhn:hasScriptStyleBroader a owl:ObjectProperty ;
    rdfs:comment "Associate an Script Style concept to its broader concept" ;
    rdfs:label "hasScriptStyleBroader" ;
    rdfs:domain mdhn:ScriptStyleType ;
    rdfs:range mdhn:ScriptStyleType .

mdhn:hasAATSubjectBroader a owl:ObjectProperty ;
    rdfs:comment "Associate an AAT Subject concept to its broader concept" ;
    rdfs:label "hasAATSubjectBroader" ;
    rdfs:domain mdhn:AATTerm ;
    rdfs:range mdhn:AATTerm .    
mdhn:hasDocumentGenre a owl:ObjectProperty ;
    rdfs:comment "Links a DigitalResource to its document gennre" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "has Document Genre" ;
    rdfs:range mdhn:DocumentGenre .

mdhn:genreUsedIn a owl:ObjectProperty ;
    rdfs:comment "Associates a genre to its associated resources" ;
    rdfs:domain mdhn:DocumentGenre ;
    rdfs:label "genre Used In" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasDocumentGenre .

mdhn:hasTemporal a owl:ObjectProperty ;
    rdfs:comment "Links a DigitalResource to Date that is just a year in YYYY formt" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "hasTemporal" ;
    rdfs:range mdhn:TemporalInfo .

mdhn:yearOfResourse a owl:ObjectProperty ;
    rdfs:comment "Associates a year to all resources that relates to it." ;
    rdfs:domain mdhn:TemporalInfo ;
    rdfs:label "yearOfResourse" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasTemporal .

mdhn:hasScriptStyle a owl:ObjectProperty ;
    rdfs:comment "Links a DigitalResource to its canvas type." ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "has Script Style" ;
    rdfs:range mdhn:ScriptStyleType .

mdhn:scriptStyleInstance a owl:ObjectProperty ;
    rdfs:comment "Links a specified script style type to its instance in a DigitalResource." ;
    rdfs:domain mdhn:ScriptStyleType ;
    rdfs:label "scriptStyleInstance" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasScriptStyle .

mdhn:hasCanvasType a owl:ObjectProperty ;
    rdfs:comment "Links a DigitalResource to its canvas type." ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "has canvas type" ;
    rdfs:range mdhn:CanvasType .

    
mdhn:resourcesOfCanvasType a owl:ObjectProperty ;
    rdfs:comment "Links a canvas to its associated resources." ;
    rdfs:domain mdhn:CanvasType ;
    rdfs:label "resources Of Canvas Type" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasCanvasType .

mdhn:hasICSubject a owl:ObjectProperty ;
    rdfs:comment "Links a Graphic subjects in DigitalResources to Iconography Subjects Resource" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "has Iconography" ;
    rdfs:range mdhn:ICSubjectSource . 

mdhn:iconographyUsedIn a owl:ObjectProperty ;
    rdfs:comment "Links a canvas to its iconography resources." ;
    rdfs:domain mdhn:ICSubjectSource ;
    rdfs:label "iconography Used In" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasICSubject .       

mdhn:ofType a owl:ObjectProperty ;
    rdfs:comment "Associates a DigitalResource with its resource type." ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "Of Type" ;
    rdfs:range mdhn:ResourceType .

mdhn:hasTypeInstance a owl:ObjectProperty ;
    rdfs:comment "Associates Resource Type to instances." ;
    rdfs:domain mdhn:ResourceType ;
    rdfs:label "has Type Instance" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:ofType .

mdhn:PublishedBy a owl:ObjectProperty ;
    rdfs:comment "Links a DigitalResource to its publisher." ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "Published By" ;
    rdfs:range mdhn:Publisher .

mdhn:hasUrl a owl:DatatypeProperty ;
    rdfs:comment "The URL of a ResourceCollection or DigitalResource." ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( mdhn:ResourceCollection mdhn:DigitalResource )
    ] ;
    rdfs:label "has URL" ;
    rdfs:range xsd:anyURI .

mdhn:icWikiDataURL a owl:DatatypeProperty ;
    rdfs:comment "URL Of Iconograpgy source in WikiData" ;
    rdfs:domain mdhn:ICSubjectSource ;
    rdfs:label "icWikiDataURL" ;
    rdfs:range xsd:anyURI  .

mdhn:agentialWikiData a owl:DatatypeProperty ;
    rdfs:comment "URL Of Agential source in WikiData" ;
    rdfs:domain mdhn:AgentialInfo;
    rdfs:label "agentialWikiData" ;
    rdfs:range xsd:anyURI  .    
    

mdhn:caption a owl:DatatypeProperty ;
    rdfs:comment "A human-readable label for a resource or collection." ;
    rdfs:domain [
        a owl:Class ;
        owl:unionOf ( mdhn:ResourceCollection mdhn:DigitalResource )
    ] ;
    rdfs:label "caption" ;
    rdfs:range xsd:string .

mdhn:canvasCount a owl:DatatypeProperty ;
    rdfs:comment "Number of canvases in each resource manifest." ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "Canvas Count" ;
    rdfs:range xsd:integer .

mdhn:folioHasDrawing a owl:DatatypeProperty ;
    rdfs:comment "Folio has Drawing?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "folioHasDrawing" ;
    rdfs:range xsd:boolean .

mdhn:folioHasTable a owl:DatatypeProperty ;
    rdfs:comment "Folio has Table?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "folioHasTable" ;
    rdfs:range xsd:boolean .

mdhn:folioIsCover a owl:DatatypeProperty ;
    rdfs:comment "Folio is cover?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "folioIsCover" ;
    rdfs:range xsd:boolean .

mdhn:folioIsColophon a owl:DatatypeProperty ;
    rdfs:comment "Folio is colophon?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "folioIsColophon" ;
    rdfs:range xsd:boolean .

mdhn:foliohasDiagram a owl:DatatypeProperty ;
    rdfs:comment "Folio has diagram?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "foliohasDiagram" ;
    rdfs:range xsd:boolean .

mdhn:folioIsOpening a owl:DatatypeProperty ;
    rdfs:comment "Folio is opening page?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "folioIsOpening" ;
    rdfs:range xsd:boolean .

mdhn:folioIsFlyLeaf a owl:DatatypeProperty ;
    rdfs:comment "Folio is flyleaf?" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "folioIsFlyLeaf" ;
    rdfs:range xsd:boolean .

mdhn:isInCollection a owl:ObjectProperty ;
    rdfs:comment "Specify the immediate collection of the resource" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "is In Collection" ;
    rdfs:range mdhn:ResourceCollection .

mdhn:hasResource a owl:ObjectProperty ;
    rdfs:comment "Links a ResourceCollection to its DigitalResource." ;
    rdfs:domain mdhn:ResourceCollection ;
    rdfs:label "has resource" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:isInCollection .

mdhn:hasPublished a owl:ObjectProperty ;
    rdfs:comment "Links a publisher to DigitalResource." ;
    rdfs:domain mdhn:Publisher ;
    rdfs:label "has Published" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:PublishedBy .

mdhn:createResources a owl:ObjectProperty ;
    rdfs:comment "Links a Creator to DigitalResource." ;
    rdfs:domain mdhn:Creator ;
    rdfs:label "creat eResources" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasCreator .

mdhn:subCollectionOf a owl:ObjectProperty ;
    rdfs:comment "Links a subCollection to its parrent Collection." ;
    rdfs:domain mdhn:ResourceCollection ;
    rdfs:label "sub Collection Of" ;
    rdfs:range mdhn:ResourceCollection .

mdhn:parentCollectionOf a owl:ObjectProperty ;
    rdfs:comment "Associates a parent Collection to its subCollections." ;
    rdfs:domain mdhn:ResourceCollection ;
    rdfs:label "parent Collection Of" ;
    rdfs:range mdhn:ResourceCollection ;
    owl:inverseOf mdhn:subCollectionOf .

mdhn:partOf a owl:ObjectProperty ;
    rdfs:comment "Links a ResourceCollection to it's parent" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "part Of" ;
    rdfs:range mdhn:DepartedCollection .

mdhn:contains a owl:ObjectProperty ;
    rdfs:comment "Links a ResourceCollection to it's childs" ;
    rdfs:domain mdhn:DepartedCollection ;
    rdfs:label "contains" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:partOf .

mdhn:hasSubject a owl:ObjectProperty ;
    rdfs:comment "Resource associate to SubjectSource(AAT,LCSH,TGM) as headings" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "hasSubject" ;
    rdfs:range mdhn:SubjectSource .

mdhn:usedSubject a owl:ObjectProperty ;
    rdfs:comment "Indicates Resources that used this specified SubjectSource(AAT,LCSH,TGM)" ;
    rdfs:domain mdhn:SubjectSource ;
    rdfs:label "usedSubject" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasSubject .

mdhn:hasTGMBroader a owl:ObjectProperty ;
    rdfs:comment "Associate a LCTGM concept to its broader concept" ;
    rdfs:label "hasTGMBroader" ;
    rdfs:domain mdhn:LCTGMSubject ;
    rdfs:range mdhn:LCTGMSubject .

mdhn:hasTGMNarrower a owl:ObjectProperty ;
    rdfs:comment "Associate a LCTGM concept to its narrower concept" ;
    rdfs:label "hasTGMNarrower" ;
    owl:inverseOf mdhn:hasTGMBroader ;
    rdfs:domain mdhn:LCTGMSubject ;
    rdfs:range mdhn:LCTGMSubject .

mdhn:hasBroaderDocGenre a owl:ObjectProperty ;
    rdfs:comment "Associate a Document Genre  to its broader genre" ;
    rdfs:label "hasBroaderDocGenre" ;
    rdfs:domain mdhn:DocumentGenre ;
    rdfs:range mdhn:DocumentGenre .

mdhn:hasNarrowerGenre a owl:ObjectProperty ;
    rdfs:comment "Associate a Document Genre to its narrower genre" ;
    rdfs:label "hasNarrowerGenre" ;
    owl:inverseOf mdhn:hasBroaderDocGenre ;
    rdfs:domain mdhn:DocumentGenre ;
    rdfs:range mdhn:DocumentGenre .

mdhn:lcTGMURI a owl:DatatypeProperty ;
    rdfs:comment "The LCTGM URI is used in LC TGM" ;
    rdfs:domain mdhn:LCTGMSubject ;
    rdfs:label "lcTGMURI" ;
    rdfs:range xsd:string .

mdhn:hasTGNPlace a owl:ObjectProperty ;
    rdfs:comment "TGN entry associate the resource to Getty TGN" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:label "hasTGNPlace" ;
    rdfs:range mdhn:GettyTGN .

mdhn:usedTGN a owl:ObjectProperty ;
    rdfs:comment "Indicates Resources that used this specified TGN" ;
    rdfs:domain mdhn:GettyTGN ;
    rdfs:label "usedTGN" ;
    rdfs:range mdhn:DigitalResource ;
    owl:inverseOf mdhn:hasTGNPlace .

mdhn:gettyTGNURI a owl:DatatypeProperty ;
    rdfs:comment "The TGN URI is used in Getty AAT" ;
    rdfs:domain mdhn:GettyTGN ;
    rdfs:label "gettyTGNURI" ;
    rdfs:range xsd:string .

mdhn:hasTGNNarrower a owl:ObjectProperty ;
    rdfs:comment "Indicates broader concept of specified TGN" ;
    rdfs:label "hasTGNNarrower" ;
    owl:inverseOf mdhn:hasTGNBroader ;
    so:domainIncludes mdhn:GettyTGN ;
    so:rangeIncludes mdhn:GettyTGN .

mdhn:hasTGNBroader a owl:ObjectProperty ;
    rdfs:comment "Associate a TGN concept to its broader concept" ;
    rdfs:label "hasTGNBroader" ;
    rdfs:domain mdhn:GettyTGN ;
    rdfs:range mdhn:GettyTGN .

mdhn:hasAATBroader a owl:ObjectProperty ;
    rdfs:comment "Associate an AAT concept to its broader concept" ;
    rdfs:label "hasAATBroader" ;
    rdfs:domain mdhn:AATTerm ;
    rdfs:range mdhn:AATTerm .

mdhn:isGuideTerm a owl:DatatypeProperty ;
    rdfs:comment "Flag to indicate if the AAT term is a guide term" ;
    rdfs:domain mdhn:AATTerm ;
    rdfs:label "isGuideTerm" ;
    rdfs:range xsd:boolean .

mdhn:hasAgential a owl:ObjectProperty ;
    rdfs:comment "Indicates that resource has Agential info associated to a person" ;
    rdfs:label "hasAgential" ;
    rdfs:domain mdhn:DigitalResource ;
    rdfs:range mdhn:AgentialInfo .

mdhn:hasRoleInResource a owl:ObjectProperty ;
    rdfs:comment "Indicates a person has atleast one role in resource" ;
    rdfs:label "hasRoleInResource" ;
    owl:inverseOf mdhn:hasAgential ;
    rdfs:domain mdhn:AgentialInfo ;
    rdfs:range mdhn:DigitalResource .


mdhn:SubjectSource a owl:Class ;
    rdfs:comment "Root class of all Subject Sources" ;
    rdfs:label "SubjectSource" .


fhkb:DomainEntity a owl:Class .

fhkb:Man a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( fhkb:Person [ a owl:Restriction ;
                        owl:onProperty fhkb:hasSex ;
                        owl:someValuesFrom fhkb:Male ] ) ] .

fhkb:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( fhkb:Person [ a owl:Restriction ;
                        owl:onProperty fhkb:hasSex ;
                        owl:someValuesFrom fhkb:Female ] ) ] .

fhkb:Person a owl:Class ;
    rdfs:subClassOf 
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasMother ;
            owl:someValuesFrom fhkb:Woman ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass fhkb:Person ;
            owl:onProperty fhkb:hasParent ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasFather ;
            owl:someValuesFrom fhkb:Man ],
        [ a owl:Restriction ;
            owl:onProperty fhkb:hasSex ;
            owl:someValuesFrom fhkb:Sex ],
        fhkb:DomainEntity ;
    owl:disjointWith fhkb:Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Man fhkb:Woman ) ] .

fhkb:Marriage a owl:Class ;
    rdfs:subClassOf fhkb:DomainEntity .

fhkb:Male a owl:Class ;
    rdfs:subClassOf fhkb:Sex .

fhkb:Female a owl:Class ;
    rdfs:subClassOf fhkb:Sex ;
    owl:disjointWith fhkb:Male .

fhkb:Sex a owl:Class ;
    rdfs:subClassOf fhkb:DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( fhkb:Female fhkb:Male ) ] .

fhkb:Ancestor a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( fhkb:Person [ a owl:Restriction ;
                        owl:onProperty fhkb:isAncestorOf ;
                        owl:someValuesFrom fhkb:Person ] ) ] .

fhkb:hasFemalePartner a owl:ObjectProperty ;
    rdfs:range fhkb:Woman ;
    rdfs:domain fhkb:Marriage ;
    rdfs:subPropertyOf fhkb:hasPartner ;
    owl:inverseOf fhkb:isFemalePartnerIn .

fhkb:hasMalePartner a owl:ObjectProperty ;
    rdfs:range fhkb:Man ;
    rdfs:domain fhkb:Marriage ;
    rdfs:subPropertyOf fhkb:hasPartner ;
    owl:inverseOf fhkb:isMalePartnerIn .

fhkb:isFatherOf a owl:ObjectProperty .

fhkb:isMotherOf a owl:ObjectProperty .

fhkb:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain fhkb:Man ;
    rdfs:range fhkb:Person ;
    rdfs:subPropertyOf fhkb:isSiblingOf .

fhkb:isSisterOf a owl:ObjectProperty ;
    rdfs:domain fhkb:Woman ;
    rdfs:range fhkb:Person ;
    rdfs:subPropertyOf fhkb:isSiblingOf .

fhkb:hasHusband a owl:ObjectProperty ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasSpouse ;
    owl:propertyChainAxiom ( fhkb:isFemalePartnerIn fhkb:hasMalePartner ) .

fhkb:hasWife a owl:ObjectProperty ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasSpouse ;
    owl:propertyChainAxiom ( fhkb:isMalePartnerIn fhkb:hasFemalePartner ) .

fhkb:isHusbandOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasHusband .

fhkb:isWifeOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasWife .

fhkb:isPartnerIn a owl:ObjectProperty .

fhkb:hasPartner a owl:ObjectProperty ;
    rdfs:domain fhkb:Marriage ;
    rdfs:range fhkb:Person ;
    owl:inverseOf fhkb:isPartnerIn .

fhkb:isSpouseOf a owl:ObjectProperty .

fhkb:hasSpouse a owl:ObjectProperty ;
    owl:inverseOf fhkb:isSpouseOf .

fhkb:isFemalePartnerIn a owl:ObjectProperty .

fhkb:isMalePartnerIn a owl:ObjectProperty .

fhkb:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:subPropertyOf fhkb:isBloodrelationOf ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:isParentOf ) .

fhkb:hasChild a owl:ObjectProperty .

fhkb:isChildOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasChild .

fhkb:hasDaughter a owl:ObjectProperty ;
    rdfs:subPropertyOf fhkb:hasChild .

fhkb:hasSon a owl:ObjectProperty ;
    rdfs:subPropertyOf fhkb:hasChild .

fhkb:isDaughterOf a owl:ObjectProperty ;
    rdfs:subPropertyOf fhkb:isChildOf ;
    owl:inverseOf fhkb:hasDaughter .

fhkb:isSonOf a owl:ObjectProperty ;
    rdfs:subPropertyOf fhkb:isChildOf ;
    owl:inverseOf fhkb:hasSon .

fhkb:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isFatherOf .

fhkb:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasParent ;
    owl:inverseOf fhkb:isMotherOf .

fhkb:hasParent a owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person ;
    rdfs:subPropertyOf fhkb:hasAncestor ;
    owl:equivalentProperty fhkb:isChildOf ;
    owl:inverseOf fhkb:isParentOf .

fhkb:isParentOf a owl:ObjectProperty .

fhkb:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Sex .

fhkb:isAncestorOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasAncestor .

fhkb:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person .

fhkb:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:subPropertyOf fhkb:hasRelation .

fhkb:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:subPropertyOf fhkb:hasRelation .

fhkb:hasUncle a owl:ObjectProperty ;
    owl:inverseOf fhkb:isUncleOf .

fhkb:isUncleOf a owl:ObjectProperty ;
    rdfs:domain fhkb:Man ;
    rdfs:range fhkb:Person ;
    owl:propertyChainAxiom ( fhkb:isBrotherOf fhkb:isParentOf ) .

fhkb:hasGreatUncle a owl:ObjectProperty ;
    owl:inverseOf fhkb:isGreatUncleOf .

fhkb:isGreatUncleOf a owl:ObjectProperty ;
    rdfs:domain fhkb:Man ;
    rdfs:range fhkb:Person ;
    owl:propertyChainAxiom ( fhkb:isBrotherOf fhkb:isGrandParentOf ) .

fhkb:hasAunt a owl:ObjectProperty ;
    owl:inverseOf fhkb:isAuntOf .

fhkb:isAuntOf a owl:ObjectProperty ;
    rdfs:domain fhkb:Woman ;
    rdfs:range fhkb:Person ;
    owl:propertyChainAxiom ( fhkb:isSisterOf fhkb:isParentOf ) .

fhkb:hasGreatAunt a owl:ObjectProperty ;
    owl:inverseOf fhkb:isGreatAuntOf .

fhkb:isGreatAuntOf a owl:ObjectProperty ;
    rdfs:domain fhkb:Woman ;
    rdfs:range fhkb:Person ;
    owl:propertyChainAxiom ( fhkb:isSisterOf fhkb:isGrandParentOf ) .

fhkb:isCousinOf a owl:ObjectProperty ;
    rdfs:subPropertyOf fhkb:isBloodrelationOf .

fhkb:isFirstCousinOf a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:subPropertyOf fhkb:isCousinOf ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:isSiblingOf fhkb:isParentOf ) .

fhkb:isSecondCousinOf a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:subPropertyOf fhkb:isCousinOf ;
    owl:propertyChainAxiom ( fhkb:hasGrandParent fhkb:isSiblingOf fhkb:isGrandParentOf ) .

fhkb:isThirdCousinOf a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:subPropertyOf fhkb:isCousinOf ;
    owl:propertyChainAxiom ( fhkb:hasGreatGrandParent fhkb:isSiblingOf fhkb:isGreatGrandParentOf ) .

fhkb:isGrandfatherOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasGrandfather .

fhkb:isGrandmotherOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasGrandmother .

fhkb:isGrandParentOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasGrandParent .

fhkb:hasGrandfather a owl:ObjectProperty ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasGrandParent ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:hasFather ) .

fhkb:hasGrandmother a owl:ObjectProperty ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasGrandParent ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:hasMother ) .

fhkb:hasGrandParent a owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person ;
    rdfs:subPropertyOf fhkb:hasAncestor ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:hasParent ) .

fhkb:isGreatGrandfatherOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasGreatGrandfather .

fhkb:isGreatGrandmotherOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasGreatGrandmother .

fhkb:isGreatGrandParentOf a owl:ObjectProperty ;
    owl:inverseOf fhkb:hasGreatGrandParent .

fhkb:hasGreatGrandfather a owl:ObjectProperty ;
    rdfs:range fhkb:Man ;
    rdfs:subPropertyOf fhkb:hasGreatGrandParent ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:hasGrandfather ) .

fhkb:hasGreatGrandmother a owl:ObjectProperty ;
    rdfs:range fhkb:Woman ;
    rdfs:subPropertyOf fhkb:hasGreatGrandParent ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:hasGrandmother ) .

fhkb:hasGreatGrandParent a owl:ObjectProperty ;
    rdfs:domain fhkb:Person ;
    rdfs:range fhkb:Person ;
    rdfs:subPropertyOf fhkb:hasAncestor ;
    owl:propertyChainAxiom ( fhkb:hasParent fhkb:hasParent fhkb:hasParent ) .    

```
### Graphical representation of this Ontology:

![alt text](/IIIFCollection/images/ontology.JPG)


## IIIFDexir Workflow and RDF Ontology

This repository, [IIIFCollection](https://github.com/MehranDHN/IIIFCollection), provides a dynamic, machine-readable catalog based on the International Image Interoperability Framework ([IIIF](http://iiif.org)) standards, focusing on cultural, artistic, architectural, photographic, and literary resources related to Persia (Iran). This README outlines the workflow for utilizing the RDF ontology and IIIF Multipart Collections, highlights the distinction between **Departed Collections** and **Resource Collections**, and provides sample SPARQL queries to interact with the Knowledge Graph.

Class Hierarchy in Ontotext GraphDB:
![alt text](/IIIFCollection/images/classhierarchy.JPG)

## Overview of IIIF Multipart Collections

IIIF Multipart Collections are structured to organize digital resources hierarchically, adhering to IIIF standards. These collections are represented as JSON-LD and are fully compatible with IIIF viewers like Mirador and OpenSeaDragon. The collections are designed to be both machine-readable and human-usable, supporting flexible data enrichment from external sources (e.g., XML, JSON, RDF Turtle) and alignment with controlled vocabularies such as Getty's AAT, TGN, Library of Congress's TGM, Schema.org, and Wikidata.

### Key Features of IIIF Multipart Collections
- **Hierarchical Structure**: Collections can contain nested sub-collections and IIIF Manifests, enabling a tree-like organization of resources.
- **Machine Readability**: JSON-LD format ensures compatibility with semantic web technologies.
- **Public Accessibility**: Resources are accessible online via standard IIIF viewers.
- **Dynamic Enrichment**: External data sources can be integrated to enhance metadata, often referenced via the `seeAlso` field in manifests.

## Refering to Contents
All the entries in this projectd designed as an IIIF Collection. Collection and Manifest are first level objects in IIIF Ecosystem and Canvasses are special type of object that typically can be integrated inside of a manifest. Refereing to Collection and manifest can be achived by `iiif-content` Query string in standard IIIF Viewers.
Thanks to IIIF Content State API we can use this method to access a canvas inside the manifest with a little differences.

### Accessing the root collection using Theseus: 
```
https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/IIIF2Collection.json
  
```
[Root Collection using Theseus](https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/IIIF2Collection.json)

### Accessing the Edward Brown Collection:
```
https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/EdwardBrowneCollection.json
  
```
[Edward Brown Collection using Theseus](https://theseusviewer.org/?iiif-content=https://raw.githubusercontent.com/MehranDHN/IIIFCollection/refs/heads/master/IIIFCollection/EdwardBrowneCollection.json)

### Accessing specified region of an image using Content State API:


```json
{
    "id": "https://manifest.storiiies-editor.cogapp.com/v3/3e7uh/Sadi-and-the-Youth-of-Kashgar/canvases/1#xywh=3357,1820,1745,1042",
    "type": "Canvas",
    "partOf": [
        {
            "id": "https://manifest.storiiies-editor.cogapp.com/v3/3e7uh/Sadi-and-the-Youth-of-Kashgar",
            "type": "Manifest"
        }
    ]
}  
```

### base64url encoded of previoud data:
```
eyJpZCI6Imh0dHBzOi8vbWFuaWZlc3Quc3RvcmlpaWVzLWVkaXRvci5jb2dhcHAuY29tL3YzLzNlN3VoL1NhZGktYW5kLXRoZS1Zb3V0aC1vZi1LYXNoZ2FyL2NhbnZhc2VzLzEjeHl3aD0zMzU3LDE4MjAsMTc0NSwxMDQyIiwidHlwZSI6IkNhbnZhcyIsInBhcnRPZiI6W3siaWQiOiJodHRwczovL21hbmlmZXN0LnN0b3JpaWllcy1lZGl0b3IuY29nYXBwLmNvbS92My8zZTd1aC9TYWRpLWFuZC10aGUtWW91dGgtb2YtS2FzaGdhciIsInR5cGUiOiJNYW5pZmVzdCJ9XX0=
```

[Specified region inside a canvas using Theseus](https://theseusviewer.org/?iiif-content=eyJpZCI6Imh0dHBzOi8vbWFuaWZlc3Quc3RvcmlpaWVzLWVkaXRvci5jb2dhcHAuY29tL3YzLzNlN3VoL1NhZGktYW5kLXRoZS1Zb3V0aC1vZi1LYXNoZ2FyL2NhbnZhc2VzLzEjeHl3aD0zMzU3LDE4MjAsMTc0NSwxMDQyIiwidHlwZSI6IkNhbnZhcyIsInBhcnRPZiI6W3siaWQiOiJodHRwczovL21hbmlmZXN0LnN0b3JpaWllcy1lZGl0b3IuY29nYXBwLmNvbS92My8zZTd1aC9TYWRpLWFuZC10aGUtWW91dGgtb2YtS2FzaGdhciIsInR5cGUiOiJNYW5pZmVzdCJ9XX0=)

### Online base64url encoder: 
- [Online Encoder](https://simplycalc.com/base64url-encode.php)

- Screenshot of a demo representing using  Content State API to access a specified region in a canvas inside an annotated manifest:
![Query 4](/IIIFCollection/images/content_state.JPG)


### RDF Ontology: Departed Collections vs. Resource Collections

The RDF ontology, implemented in Turtle format, models two primary entities: **ResourceCollection** and **DigitalResource**, alongside other classes like `Creator`, `Publisher`, `ResourceType`, and `CanvasType`. Below, we differentiate between **Departed Collections** and **Resource Collections**:

### Departed Collections
- **Purpose**: Designed to integrate digital resources scattered across various institutions, such as museums or archives worldwide.
- **Characteristics**: 
  - Aggregates resources that are not necessarily related by subject but are unified by their cultural or historical significance to Persia.
  - Facilitates interoperability by linking disparate digital assets into a cohesive collection.
  - Often references external sources via the `seeAlso` field for additional metadata.
- **Use Case**: A Departed Collection might include manuscripts from a museum in London, photographs from an archive in Tehran, and books from a library in New York, unified under a shared cultural theme.

### Resource Collections
- **Purpose**: Organized by specific subjects (e.g., Persian architecture, calligraphy, or literature) with a hierarchical structure based on IIIF Collection capabilities.
- **Characteristics**:
  - Follows a tree-like organization where collections can contain sub-collections and manifests.
  - Aligned with controlled vocabularies (e.g., AAT, TGM, Wikidata) to categorize resources by type or theme.
  - Emphasizes structured, subject-based access to resources for both human and machine consumption.
- **Use Case**: A Resource Collection might focus on "Persian Miniature Paintings," with sub-collections for different artists or periods, each containing relevant IIIF Manifests.

### Ontology Representation
The ontology defines relationships such as `hasResource`, `hasCreator`, `hasPublisher`, and `hasResourceType` to link entities. For example:
- `mdhn:ResourceCollection` represents both Departed and Resource Collections, with `mdhn:partOf` indicating hierarchical relationships.
- `mdhn:DigitalResource` represents individual IIIF Manifests, linked to collections via `mdhn:belongsTo`.

### Transforming RDF Ontology to First-Order Logic

RDF ontologies can be translated into First-Order Logic (FOL) to enable formal reasoning, theorem proving, or integration with logical systems. In FOL, classes are represented as unary predicates (e.g., `ResourceCollection(x)`), while properties are binary predicates (e.g., `hasResource(x, y)`). Domain and range constraints are axiomatized using universal quantifiers to enforce type restrictions. Inverse properties are captured with equivalence axioms.

Below, we transform the key elements of the RDF ontology into FOL axioms, with a strong emphasis on the domain and range of each object and datatype property. Note that namespaces (e.g., `mdhn:`) are omitted for brevity in the predicates, but they align with the Turtle definitions.

### Classes as Unary Predicates
- `ResourceCollection(x)`: True if x is a resource collection.
- `DigitalResource(x)`: True if x is a digital resource (IIIF Manifest).
- `Creator(x)`: True if x is a creator entity.
- `Publisher(x)`: True if x is a publisher entity.
- `ResourceType(x)`: True if x is a resource type (aligned with vocabularies like AAT).
- `CanvasType(x)`: True if x is a canvas type within a manifest.

### Object Properties with Domain and Range
Each object property is represented as a binary predicate, with axioms for domain (subject type) and range (object type). Inverse relationships are also axiomatized.

- **hasResource(x, y)**  
  - Domain: ResourceCollection (∀x ∀y (hasResource(x, y) → ResourceCollection(x)))  
  - Range: DigitalResource (∀x ∀y (hasResource(x, y) → DigitalResource(y)))  
  - Inverse: belongsTo(y, x) (∀x ∀y (hasResource(x, y) ↔ belongsTo(y, x)))

- **hasCreator(x, y)**  
  - Domain: DigitalResource (∀x ∀y (hasCreator(x, y) → DigitalResource(x)))  
  - Range: Creator (∀x ∀y (hasCreator(x, y) → Creator(y)))  
  - Inverse: createResources(y, x) (∀x ∀y (hasCreator(x, y) ↔ createResources(y, x)))

- **hasCanvasType(x, y)**  
  - Domain: DigitalResource (∀x ∀y (hasCanvasType(x, y) → DigitalResource(x)))  
  - Range: CanvasType (∀x ∀y (hasCanvasType(x, y) → CanvasType(y)))  
  - No inverse defined.

- **ofType(x, y)**  
  - Domain: DigitalResource (∀x ∀y (ofType(x, y) → DigitalResource(x)))  
  - Range: ResourceType (∀x ∀y (hasResourceType(x, y) → ResourceType(y)))  
  - Inverse: hasTypeInstance(y, x) (∀x ∀y (hasTypeInstance(x, y) ↔ resourceTypeInstance(y, x)))

- **hasPublisher(x, y)**  
  - Domain: DigitalResource (∀x ∀y (hasPublisher(x, y) → DigitalResource(x)))  
  - Range: Publisher (∀x ∀y (hasPublisher(x, y) → Publisher(y)))  
  - Inverse: publishedResource(y, x) (∀x ∀y (hasPublisher(x, y) ↔ publishedResource(y, x)))

- **belongsTo(x, y)**  
  - Domain: DigitalResource (∀x ∀y (belongsTo(x, y) → DigitalResource(x)))  
  - Range: ResourceCollection (∀x ∀y (belongsTo(x, y) → ResourceCollection(y)))  
  - Inverse of hasResource.

- **publishedResource(x, y)**  
  - Domain: Publisher (∀x ∀y (publishedResource(x, y) → Publisher(x)))  
  - Range: DigitalResource (∀x ∀y (publishedResource(x, y) → DigitalResource(y)))  
  - Inverse of hasPublisher.

- **createResources(x, y)**  
  - Domain: Creator (∀x ∀y (createResources(x, y) → Creator(x)))  
  - Range: DigitalResource (∀x ∀y (createResources(x, y) → DigitalResource(y)))  
  - Inverse of hasCreator.

- **resourceTypeInstance(x, y)**  
  - Domain: ResourceType (∀x ∀y (resourceTypeInstance(x, y) → ResourceType(x)))  
  - Range: DigitalResource (∀x ∀y (resourceTypeInstance(x, y) → DigitalResource(y)))  
  - Inverse of hasResourceType.

- **subCollectionOf(x, y)**  
  - Domain: ResourceCollection (∀x ∀y (subCollectionOf(x, y) → ResourceCollection(x)))  
  - Range: ResourceCollection (∀x ∀y (subCollectionOf(x, y) → ResourceCollection(y)))  
  - Inverse: parentCollectionOf(y, x) (∀x ∀y (parentCollectionOf(x, y) ↔ subCollectionOf(y, x)))

- **partOf(x, y)**  
  - Domain: DigitalResource (∀x ∀y (partOf(x, y) → DigitalResource(x)))  
  - Range: DepartedCollection (∀x ∀y (partOf(x, y) → DepartedCollection(y)))  
  - Inverse: contains(y, x) (∀x ∀y (contains(x, y) ↔ partOf(y, x)))  

### Datatype Properties with Domain and Range
Datatype properties link entities to literal values (e.g., strings or URIs).

- **hasUrl(x, y)**  
  - Domain: ResourceCollection or DigitalResource (∀x ∀y (hasUrl(x, y) → (ResourceCollection(x) ∨ DigitalResource(x))))  
  - Range: xsd:anyURI (∀x ∀y (hasUrl(x, y) → URI(y)))  
  - (Where URI(y) represents y being a URI value.)

- **caption(x, y)**  
  - Domain: ResourceCollection or DigitalResource (∀x ∀y (caption(x, y) → (ResourceCollection(x) ∨ DigitalResource(x))))  
  - Range: xsd:string (∀x ∀y (caption(x, y) → String(y)))  
  - (Where String(y) represents y being a string literal.)

These FOL axioms provide a formal foundation for reasoning about the ontology, such as checking consistency or inferring relationships. Tools like theorem provers (e.g., Vampire or E Prover) can utilize these axioms for advanced queries beyond SPARQL.

### Workflow for Using RDF Ontology and IIIF Collections

1. **Accessing the Collection**:
   - Use a standard IIIF viewer (e.g., Mirador 3.0, OSD, Thesus, ... ) to explore the collection.
   - Retrieve JSON-LD manifests or collections via their URLs.

2. **Enriching Data**:
   - Parse external sources referenced in the `seeAlso` field to enrich metadata.
   - Align resources with controlled vocabularies (e.g., AAT, TGM) for semantic consistency.

3. **Building a Knowledge Graph**:
   - Convert JSON-LD manifests into RDF Turtle format using the provided ontology.
   - Use tools like Apache Jena or RDFLib to load and query the Knowledge Graph.

4. **Querying the Knowledge Graph**:
   - Execute SPARQL queries to extract insights, such as resource types, creators, or hierarchical relationships.

5. **Analyzing and Visualizing**:
   - Generate statistics or visualizations based on query results, leveraging the machine-readable structure.
   - Use IIIF viewers for human-readable exploration.


### Sample SPARQL Queries

Below are sample SPARQL queries to demonstrate how to interact with the Knowledge Graph built from the IIIFDexir ontology.

#### Query 1: List All Digital Collections with the number of resources
This query retrieves all `mdhn:ResourceCollection` instances and counts number of `mdhn:DigitalResource` instances in each of them.

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

select  ?collection (Count(?s) as ?resourceCount){
    ?s a mdhn:DigitalResource;
    (mdhn:isInCollection)* ?collection.
    ?collection a mdhn:ResourceCollection.


}
Group by ?collection
Order by Desc(?resourceCount)
```

####  Query 2: Find Creators of Digital Resources
This query lists creators and their labels associated with `DigitalResource` instances.

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
SELECT ?resource ?creator ?label
WHERE {
  ?resource a mdhn:DigitalResource ;
            mdhn:hasCreator ?creator .
    ?creator rdfs:label ?label.
}
```

####  Query 3: Identify Hierarchical Structure of Resource Collections
This query retrieves parent-child relationships between `ResourceCollection` instances.

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
SELECT ?parent ?child ?childLabel
WHERE {
  ?child a mdhn:ResourceCollection ;
    mdhn:subCollectionOf ?parent ;
    mdhn:caption ?childLabel .
}
```

####  Query 4: Resources by Type Using Controlled Vocabularies
This query finds `DigitalResource` instances associated with a specific resource type from Getty's AAT.

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX aat: <https://vocab.getty.edu/aat/>
SELECT ?resource ?label
WHERE {
  ?resource a mdhn:DigitalResource ;
            mdhn:ofType mdhn:aat300027200 ;  # AAT term for "Photograph Album"
            rdfs:label ?label .
}
```
There is a difference between logical Collections and actual resource type. To get a full list of all members of `mdhn:PhotographAlbum` which is an instance of  `mdhn:ResourceCollection` the following Query can be use:

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

select ?s  ?reslabel{
    ?s a mdhn:DigitalResource;
       rdfs:label ?reslabel;
      mdhn:isInCollection mdhn:PhotographAlbum.

}
```

To limit the labels to specific Language:

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX aat: <https://vocab.getty.edu/aat/>
SELECT ?resource ?label
WHERE {
  ?resource a mdhn:DigitalResource ;
            mdhn:ofType mdhn:aat300027200 ;  # AAT term for "Photograph Album"
            rdfs:label ?label .
    FILTER(LANG(?label)="en")
    #BIND(LANG(?label) as ?languages)
    #FILTER(?languages IN ("fr", "en", "fa"))
}
```
Screenshot of running SPARQL query and its coresponding result:
![Query 4](/IIIFCollection/images/langfilter.JPG)

####  Query 5: Accessing the specified folio type (Drawings) 
This query finds all matches that have the `mdhn:folioHasDrawing` flag, which is a flag to identify the drawing resources.
In future improvements, we should associate this feature with the particular Controlled Vocabulary designed to identify folio types.

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX aat: <https://vocab.getty.edu/aat/>
SELECT *
WHERE {
  ?resource a mdhn:DigitalResource ; 
            mdhn:folioHasDrawing ?drawing;
            mdhn:partOf ?part;
            rdfs:label ?label .
}
```
![Query 5](/IIIFCollection/images/FolioType.JPG)
It is obvious that we can use filters to limit the results only for specified physical or logical collection:

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX aat: <https://vocab.getty.edu/aat/>
SELECT *
WHERE {
  ?resource a mdhn:DigitalResource ; 
            mdhn:folioHasDrawing ?drawing;
            mdhn:partOf ?part;
            rdfs:label ?label .
  Filter(?part=mdhn:vcol1000111)
}
```
####  Query 6: Accessing the resources that somehow related to specified geo spatial TGN location
This query finds all resources that related to specified TGN location based on  `mdhn:hasTGNPlace` predicate. We also `mdhn:ofType` predicate as another dimension to find the resource types.
This query can be easily extended to group the results by resource types to count the resources associated to each type. 
The `mdhn:tgn1001228` is the part of the Isfahan URI which we reconciliate with the Getty's TGN .
See [TGN](http://vocab.getty.edu/tgn/1001228)

```sparql
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>
select ?s  ?place ?restype ?typelbl {
    ?s a mdhn:DigitalResource;
      mdhn:ofType ?restype;
      mdhn:hasTGNPlace ?place.
    ?restype rdfs:label ?typelbl.
    Filter(?place=mdhn:tgn1001228)
    Filter(Lang(?typelbl)="en")
}
```

####  Query 7: Using agential info of the resources
This query finds all resources that marked with Agential information which is instances of  `fhkb:Person`. Those resources associate with `mdhn:hasAgential` predicate to the Agential info which is Adapted from FHKB.

See [Family History Knowledge Base (FHKB)](https://oboacademy.github.io/obook/tutorial/fhkb/)

```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

select ?person ?lblPerson{
    ?s a mdhn:DigitalResource;
       mdhn:hasAgential ?person.
    ?person rdfs:label ?lblPerson.
    Filter(Lang(?lblPerson)="fa")
}
```
![Query 7](/IIIFCollection/images/fhkbResult.JPG)

Accessing all resources that relate to specified person:
```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

select ?person ?lblPerson{
    ?s a mdhn:DigitalResource;
       mdhn:hasAgential ?person.
    ?person rdfs:label ?lblPerson.
    Filter(?person=mdhn:Naser_al_Din_Shah_Qajar)
    Filter(Lang(?lblPerson)="fa")
}
```
####  Query 8: Accessing the resources that have Kufic script style excepts those in specified collection
This query finds all resources that has specified  `mdhn:aat300194434` script style which is Kufic script in AAT Thesaurus. We limit the results to all but those that are in specified Collection `mdhn:AsarolBaghieOrMs161`.


```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>
# ليست آثاری که به خط کوفی مرتبط هستند به استثنای مجموعه آثار الباقيه
select * {
    ?s a mdhn:DigitalResource;
       mdhn:hasScriptStyle mdhn:aat300194434;
       mdhn:isInCollection ?collection.
    Filter(?collection!=mdhn:AsarolBaghieOrMs161)
  
}
```
####  Query 9: Determinig which resources have the Subject headers that reconciliated against AAT and LCSH (Not The LCTGM)
This query finds all resources that have specified subject header types. Those that are `mdhn:AATTerm` and `mdhn:LCSHSubject` because all resources reconciliate against three primary sources inclusing `LCTGM`, `LCSH` and `AAT`.
```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT *
WHERE {
    ?s a mdhn:DigitalResource ;
       mdhn:hasSubject ?subject ;
       mdhn:isInCollection ?collection .
    ?subject a ?type .
    FILTER(?type IN (mdhn:AATTerm, mdhn:LCSHSubject))
}
```
####  Query 10: Determinig the participants in resources with their roles 
This query finds all participants who involve somehow in resources. Roles such as `mdhn:hasParticipantInRolePhotographer` and `mdhn:hasParticipantInRoleIllustrator` are Object Properties which are `rdfs:subPropertyOf` the `mdhn:hasParticipantInRole` that enables us to integrate all participants of Digital Resources in an effective way.
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

SELECT *
WHERE {
    ?s a mdhn:DigitalResource ;
       mdhn:hasParticipantInRole ?Agential ;
       mdhn:isInCollection ?collection .
}
```
Obviously we can get all participants with one or more specified role:
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

SELECT *
WHERE {
    ?s a mdhn:DigitalResource ;
       mdhn:hasParticipantInRolePhotographer ?Agential ;
       mdhn:isInCollection ?collection .
}
```
Then execuating a query to get a result of aggregated agential info:
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

SELECT Distinct ?agential (Count(?s) as ?cs)
WHERE {
    ?s a mdhn:DigitalResource ;
       mdhn:hasParticipantInRole ?agential ;
       mdhn:isInCollection ?collection .
   
}
GROUP BY ?agential
```

####  Query 11: Filter the resources in specified physical collections based on particular Iconography Tag
This query finds all digital resources that has a particular Tag in specified Collection. This can be achieved with a combinations of  `mdhn:isInCollection` and `mdhn:depicts` and then using a `Filter` to narrow the result.
```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

select * {
    ?s a mdhn:DigitalResource;
       mdhn:isInCollection mdhn:DepartedDrawing;
       mdhn:depicts ?icgtag.
    ?icgtag rdfs:label ?lbltag.
    Filter(Lang(?lbltag)="en")
    Filter(?icgtag=mdhn:Boat)
}
```

####  Query 12: Filter the resources in specified physical collections based on particular Agential info and his involvement role and narrowing the result to those have valid Iconography Tag
This query finds all digital resources that has a particular Tag in specified Collection. This can be achieved with a combinations of  `mdhn:isInCollection` ,`mdhn:depicts` and `mdhn:hasParticipantInRolePoet` and then using a `Filter` to narrow the result.
```sparql
PREFIX mdhn: <http://example.com/mdhn/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <https://schema.org/>

select *{
    ?s a mdhn:DigitalResource;
       mdhn:isInCollection mdhn:DepartedDrawing;
       mdhn:depicts ?iconography;
       mdhn:hasParticipantInRolePoet ?poet.
    ?s rdfs:label ?lblresource.
    Filter(Lang(?lblresource)="en")
    Filter(?poet=mdhn:Abul_Qasim_Firdawsi)
}
```
## On-the-Fly IIIF Manifest Generator
A flexible Python script that dynamically combines selected IIIF manifests into a single, local-compatible manifest (Presentation API 2.0 or 3.0).
Supports:

- Multiple sources with different base URLs and API versions
- Selecting specific canvases (by zero-based index) from each manifest
- Custom canvas labels using a user-defined template
- Optional table of contents (structures/ranges)
- Custom metadata (completely independent of source manifests)
- Mixed v2 and v3 source manifests (with annotation normalization)
- Detailed logging & validation to debug problems

This tool is particularly useful for creating curated selections from heterogeneous IIIF collections (e.g. mixing archive.org HV.* items with Chester Beatty Library Persian manuscripts or any other IIIF endpoints).


## Getting Started

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MehranDHN/IIIFCollection.git
   ```

2. **Explore the Collection**:
   - Open the collection in a IIIF viewer like Mirador.
   - Inspect JSON-LD files for manifests and collections.

3. **Work with the Ontology**:
   Creating a full GraphDB from the data that have provided required using a Local or Cloud GraphDB System. Ontotext Graph and Stardog Cloud Service are excellent choices.
   - Load the Turtle ontology (`iiifCollectionOntology.ttl`) into a triplestore (e.g., Apache Jena).
   - Load the Turtle (`aat_hierarchy.ttl`) which is a subset of the Standard AAT for the scope of this project.
   - Load the Turtle (`iconography_RDF.ttl`) which is a limited-scope for iconography based on WikiData.   
   - Load the Turtle (`ctl_vocabs.ttl`) which is a subset of Controlled Vocabularies.   
   - Load the Turtle (`LCTGM_RDF.ttl`), (`tgn_subset_updated.ttl`) and (`PersonsRDFData.ttl`).
   - Load the (`resources.ttl`) which is actual RDF data of the collection.      
   - Use SPARQL queries to analyze the Knowledge Graph.

4. **Contribute**:
   - Enrich the collection by adding new manifests or external metadata.
   - Help to better organizing the categorizations.
   - Submit pull requests for ontology updates or new SPARQL queries.

## Notes
- The catalog is dynamic and may undergo daily updates to its structure and contents.
- Ensure proper parsing of `seeAlso` fields to incorporate external metadata.
- The ontology is designed to be extensible, allowing integration with additional vocabularies or data sources.

## About
This project is a dynamic IIIF collection featuring a hierarchical catalog related to the culture, art, architecture, photographs, and books of Persia (Iran). It aims to provide a machine-readable, semantically rich resource for researchers, developers, and enthusiasts.


---
*Updated on Nov 7, 2025, by **MehranDHN**, powered by: Grok 3 (xAI).*
