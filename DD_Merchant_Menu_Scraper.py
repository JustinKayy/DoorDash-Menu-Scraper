import requests
import json 


storeId = str(input('What is the DD store ID? '))           #allow user to input the DD store/menu ID
menuId = str(input('What is the DD menu ID? '))
cookie= input('Enter a cookie: ')


url = 'https://merchant-portal.doordash.com/mx-menu-tools-bff/graphql'
header = {
    'content-type':'application/json',
    'cookie': cookie,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
} 

##DD Queries 
menu = json.dumps({
    "operationName":"getMenu",
    "variables":{
        "menuId": menuId,"storeId": storeId
        },
    "query":"query getMenu($menuId: ID!, $storeId: ID!) {\n  getMenu(menuId: $menuId, storeId: $storeId) {\n    id\n    name\n    subtitle\n    isActive\n    isCatering\n    createdAt\n    merchantSuppliedId\n    extras {\n      ...ExtraFragment\n      __typename\n    }\n    categories {\n      ...CategoryFragment\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CategoryFragment on MenuCategory {\n  id\n  merchantSuppliedId\n  name\n  menuId\n  title: subtitle\n  subtitle\n  isActive\n  isDeactivated: isSuspended\n  sortId\n  items {\n    ...ItemFragment\n    __typename\n  }\n  __typename\n}\n\nfragment ItemFragment on MenuItem {\n  id\n  merchantSuppliedId\n  isActive\n  price\n  basePrice\n  name\n  description\n  sortId\n  minAgeRequirement\n  photoId\n  imageUrl\n  isBikeFriendly\n  menuItemNumber\n  isAlcohol\n  isDeactivated: isSuspended\n  __typename\n}\n\nfragment ExtraFragment on MenuItemExtra {\n  id\n  merchantSuppliedId\n  isActive\n  description\n  name\n  title: name\n  sortId\n  minNumOptions\n  maxNumOptions\n  numFreeOptions\n  minAggregateOptionsQuantity\n  maxAggregateOptionsQuantity\n  minOptionChoiceQuantity\n  maxOptionChoiceQuantity\n  __typename\n}\n"
    })

items = json.dumps({
  "operationName": "GetItemsForStore",
  "variables": {
    "storeId": storeId
  },
  "query": "query GetItemsForStore($storeId: ID!) {\n  getItemsForStore(storeId: $storeId) {\n    id\n    isActive\n    isSuspended\n    imageUrl\n    name\n    description\n    price\n    basePrice\n    merchantSuppliedId\n    sortId\n    extraIds\n    menuIds\n    isAlcohol\n    dailyQuantityLimit\n    category {\n      id\n      name\n      subtitle\n      __typename\n    }\n    __typename\n  }\n}\n"
})

extras = json.dumps({
    "operationName":"GetExtrasForStore",
    "variables":
    {"storeId": storeId
    },
    "query":"query GetExtrasForStore($storeId: ID!) {\n  getExtrasForStore(storeId: $storeId) {\n    id\n    isActive\n    isSuspended\n    name\n    merchantSuppliedId\n    minNumOptions\n    maxNumOptions\n    numFreeOptions\n    options {\n      id\n      name\n      sortId\n      isActive\n      description\n      basePrice\n      price\n      isSuspended\n      __typename\n    }\n    sharedBy {\n      id\n      name\n      __typename\n    }\n    __typename\n  }\n}\n"
    })


getMenu = requests.request("POST", url, headers=header, data=menu)
getItems = requests.request("POST", url, headers=header, data=items)
getExtras = requests.request("POST", url, headers=header, data=extras)

getMenu.encoding = 'UTF-8'
getItems.encoding = 'UTF-8'
getExtras.encoding = 'UTF-8'
                                                                        

Menu = getMenu.json()
Items = getItems.json()
Extras = getExtras.json()


open('Menu.json', 'w', encoding='UTF-8').write(
    json.dumps(Menu, ensure_ascii=False, indent=2))

open('Items.json', 'w', encoding='UTF-8').write(
    json.dumps(Items, ensure_ascii=False, indent=2))

open('Extras.json', 'w', encoding='UTF-8').write(
    json.dumps(Extras, ensure_ascii=False, indent=2))




